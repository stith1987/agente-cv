"""
Multi-LLM Client Module

Cliente unificado que soporta múltiples proveedores LLM usando
API compatible con OpenAI (plug-and-play).

Soporta:
- OpenAI (GPT-4, GPT-3.5)
- DeepSeek
- Groq (Mixtral, Llama)
- Google Gemini (vía endpoint compatible)
- Ollama (modelos locales)
- Anthropic Claude (vía endpoint compatible)
"""

import asyncio
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
from openai import OpenAI, AsyncOpenAI

from .config import OpenAIConfig
from .logger import AgentLogger


class LLMProvider(Enum):
    """Proveedores LLM soportados"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    GROQ = "groq"
    GEMINI = "gemini"
    OLLAMA = "ollama"
    ANTHROPIC = "anthropic"
    CUSTOM = "custom"


# Configuraciones predefinidas de proveedores
PROVIDER_ENDPOINTS = {
    "openai": "https://api.openai.com/v1",
    "deepseek": "https://api.deepseek.com/v1",
    "groq": "https://api.groq.com/openai/v1",
    "ollama": "http://localhost:11434/v1",
    # Gemini y Anthropic requieren adaptadores específicos
}


@dataclass
class LLMResponse:
    """Respuesta unificada de LLM"""
    content: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir a diccionario"""
        return {
            "content": self.content,
            "provider": self.provider,
            "model": self.model,
            "tokens_used": self.tokens_used,
            "finish_reason": self.finish_reason,
            "metadata": self.metadata or {}
        }


class MultiLLMClient:
    """
    Cliente unificado para múltiples proveedores LLM.
    
    Permite invocar diferentes modelos usando la misma interfaz
    y combinar respuestas para ensembles o comparaciones.
    """
    
    def __init__(self, config: OpenAIConfig, logger: Optional[AgentLogger] = None):
        """
        Inicializar cliente multi-LLM
        
        Args:
            config: Configuración del LLM
            logger: Logger opcional
        """
        self.config = config
        self.logger = logger or AgentLogger("multi_llm_client")
        
        # Determinar base_url según el proveedor
        if config.base_url:
            base_url = config.base_url
        else:
            base_url = PROVIDER_ENDPOINTS.get(config.provider, PROVIDER_ENDPOINTS["openai"])
        
        # Crear clientes síncronos y asíncronos
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=base_url if config.provider != "openai" else None
        )
        
        self.async_client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=base_url if config.provider != "openai" else None
        )
        
        self.logger.info(
            f"MultiLLMClient initialized",
            extra={
                "provider": config.provider,
                "model": config.model,
                "base_url": base_url
            }
        )
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generar respuesta usando el LLM configurado
        
        Args:
            messages: Lista de mensajes (formato OpenAI)
            temperature: Temperatura de generación (override)
            max_tokens: Máximo de tokens (override)
            **kwargs: Parámetros adicionales
            
        Returns:
            Respuesta del LLM
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=temperature or self.config.temperature,
                max_tokens=max_tokens or self.config.max_tokens,
                **kwargs
            )
            
            # Extraer información
            content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            tokens_used = response.usage.total_tokens if response.usage else None
            
            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                tokens_used=tokens_used,
                finish_reason=finish_reason,
                metadata={
                    "temperature": temperature or self.config.temperature,
                    "max_tokens": max_tokens or self.config.max_tokens
                }
            )
            
        except Exception as e:
            self.logger.error(
                f"Error generating response",
                exception=e,
                extra={"provider": self.config.provider, "model": self.config.model}
            )
            raise
    
    async def generate_async(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generar respuesta asíncrona
        
        Args:
            messages: Lista de mensajes (formato OpenAI)
            temperature: Temperatura de generación (override)
            max_tokens: Máximo de tokens (override)
            **kwargs: Parámetros adicionales
            
        Returns:
            Respuesta del LLM
        """
        try:
            response = await self.async_client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=temperature or self.config.temperature,
                max_tokens=max_tokens or self.config.max_tokens,
                **kwargs
            )
            
            content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            tokens_used = response.usage.total_tokens if response.usage else None
            
            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                tokens_used=tokens_used,
                finish_reason=finish_reason,
                metadata={
                    "temperature": temperature or self.config.temperature,
                    "max_tokens": max_tokens or self.config.max_tokens
                }
            )
            
        except Exception as e:
            self.logger.error(
                f"Error in async generation",
                exception=e,
                extra={"provider": self.config.provider, "model": self.config.model}
            )
            raise


class MultiLLMEnsemble:
    """
    Sistema de ensemble que invoca múltiples LLMs y combina resultados.
    
    Permite comparar outputs de diferentes modelos y seleccionar el mejor
    o crear respuestas combinadas.
    """
    
    def __init__(self, configs: List[OpenAIConfig], logger: Optional[AgentLogger] = None):
        """
        Inicializar ensemble
        
        Args:
            configs: Lista de configuraciones para diferentes LLMs
            logger: Logger opcional
        """
        self.logger = logger or AgentLogger("multi_llm_ensemble")
        self.clients = [MultiLLMClient(config, logger) for config in configs]
        
        self.logger.info(
            f"MultiLLMEnsemble initialized with {len(self.clients)} clients",
            extra={
                "providers": [c.config.provider for c in self.clients],
                "models": [c.config.model for c in self.clients]
            }
        )
    
    async def generate_ensemble(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> List[LLMResponse]:
        """
        Generar respuestas de todos los LLMs en paralelo
        
        Args:
            messages: Lista de mensajes
            temperature: Temperatura override
            max_tokens: Max tokens override
            
        Returns:
            Lista de respuestas de todos los modelos
        """
        try:
            # Generar todas las respuestas en paralelo
            tasks = [
                client.generate_async(messages, temperature, max_tokens)
                for client in self.clients
            ]
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filtrar errores
            valid_responses = []
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    self.logger.error(
                        f"Error from provider {self.clients[i].config.provider}",
                        exception=response
                    )
                else:
                    valid_responses.append(response)
            
            self.logger.info(
                f"Ensemble generated {len(valid_responses)}/{len(self.clients)} successful responses"
            )
            
            return valid_responses
            
        except Exception as e:
            self.logger.error("Error in ensemble generation", exception=e)
            raise
    
    def select_best_response(
        self,
        responses: List[LLMResponse],
        criteria: str = "length"
    ) -> LLMResponse:
        """
        Seleccionar la mejor respuesta según criterio
        
        Args:
            responses: Lista de respuestas
            criteria: Criterio de selección (length, tokens, custom)
            
        Returns:
            Mejor respuesta según criterio
        """
        if not responses:
            raise ValueError("No responses to select from")
        
        if criteria == "length":
            # Seleccionar la más completa
            best = max(responses, key=lambda r: len(r.content))
        elif criteria == "tokens":
            # Seleccionar la que usó más tokens (más detallada)
            best = max(responses, key=lambda r: r.tokens_used or 0)
        else:
            # Por defecto, primera respuesta
            best = responses[0]
        
        self.logger.info(
            f"Selected best response from {best.provider}",
            extra={"criteria": criteria, "provider": best.provider}
        )
        
        return best
    
    def combine_responses(
        self,
        responses: List[LLMResponse],
        combination_client: Optional[MultiLLMClient] = None
    ) -> str:
        """
        Combinar múltiples respuestas en una sola usando LLM
        
        Args:
            responses: Lista de respuestas a combinar
            combination_client: Cliente para la combinación (usa el primero si no se especifica)
            
        Returns:
            Respuesta combinada
        """
        if not responses:
            return ""
        
        if len(responses) == 1:
            return responses[0].content
        
        client = combination_client or self.clients[0]
        
        # Crear prompt para combinar respuestas
        responses_text = "\n\n---\n\n".join([
            f"Respuesta de {r.provider} ({r.model}):\n{r.content}"
            for r in responses
        ])
        
        combination_messages = [
            {
                "role": "system",
                "content": "Eres un experto en sintetizar información. "
                          "Combina las siguientes respuestas en una sola respuesta "
                          "coherente y completa, tomando lo mejor de cada una."
            },
            {
                "role": "user",
                "content": f"Combina estas respuestas:\n\n{responses_text}"
            }
        ]
        
        try:
            combined = client.generate(combination_messages, temperature=0.3)
            
            self.logger.info(
                f"Combined {len(responses)} responses",
                extra={"providers": [r.provider for r in responses]}
            )
            
            return combined.content
            
        except Exception as e:
            self.logger.error("Error combining responses", exception=e)
            # Fallback: devolver la primera respuesta
            return responses[0].content


# ==================== Utilidades ====================

def create_multi_llm_client(
    provider: str = "openai",
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    **kwargs
) -> MultiLLMClient:
    """
    Factory function para crear cliente Multi-LLM fácilmente
    
    Args:
        provider: Nombre del proveedor
        api_key: API key
        model: Nombre del modelo
        base_url: URL base opcional
        **kwargs: Parámetros adicionales
        
    Returns:
        Cliente Multi-LLM configurado
    """
    import os
    
    # Defaults
    api_key = api_key or os.getenv("OPENAI_API_KEY", "")
    model = model or os.getenv("OPENAI_MODEL", "gpt-4")
    
    config = OpenAIConfig(
        api_key=api_key,
        model=model,
        provider=provider,
        base_url=base_url,
        temperature=kwargs.get("temperature", 0.7),
        max_tokens=kwargs.get("max_tokens", 2000)
    )
    
    return MultiLLMClient(config)


# ==================== Ejemplos de uso ====================

if __name__ == "__main__":
    """
    Ejemplos de uso del Multi-LLM Client
    """
    
    # Ejemplo 1: Cliente único
    print("=== Ejemplo 1: Cliente OpenAI ===")
    client_openai = create_multi_llm_client(
        provider="openai",
        model="gpt-3.5-turbo"
    )
    
    response = client_openai.generate([
        {"role": "system", "content": "Eres un asistente útil."},
        {"role": "user", "content": "¿Qué es Python?"}
    ])
    print(f"Respuesta de {response.provider}: {response.content[:100]}...")
    
    # Ejemplo 2: DeepSeek
    print("\n=== Ejemplo 2: Cliente DeepSeek ===")
    client_deepseek = create_multi_llm_client(
        provider="deepseek",
        api_key="tu_deepseek_key",
        model="deepseek-chat"
    )
    
    # Ejemplo 3: Ensemble
    print("\n=== Ejemplo 3: Ensemble Multi-LLM ===")
    configs = [
        OpenAIConfig(api_key="key1", model="gpt-3.5-turbo", provider="openai"),
        OpenAIConfig(api_key="key2", model="deepseek-chat", provider="deepseek"),
        OpenAIConfig(api_key="key3", model="mixtral-8x7b", provider="groq")
    ]
    
    ensemble = MultiLLMEnsemble(configs)
    
    async def test_ensemble():
        messages = [
            {"role": "system", "content": "Eres un experto en tecnología."},
            {"role": "user", "content": "Explica qué es Kubernetes"}
        ]
        
        responses = await ensemble.generate_ensemble(messages)
        
        print(f"Recibidas {len(responses)} respuestas")
        for resp in responses:
            print(f"- {resp.provider}: {len(resp.content)} caracteres")
        
        # Seleccionar mejor
        best = ensemble.select_best_response(responses, criteria="length")
        print(f"\nMejor respuesta de: {best.provider}")
        
        # Combinar
        combined = ensemble.combine_responses(responses)
        print(f"\nRespuesta combinada: {len(combined)} caracteres")
    
    # asyncio.run(test_ensemble())
