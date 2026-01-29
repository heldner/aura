from pydantic import AliasChoices, BaseModel, Field, SecretStr


class LLMSettings(BaseModel):
    provider: str = "mistral"
    model: str = Field(
        "mistral-large-latest",
        validation_alias=AliasChoices("AURA_LLM__MODEL", "LLM_MODEL"),
    )
    api_key: SecretStr = Field(
        "",
        validation_alias=AliasChoices("AURA_LLM__API_KEY", "MISTRAL_API_KEY"),
    )
    openai_api_key: SecretStr = Field(
        "",
        validation_alias=AliasChoices("AURA_LLM__OPENAI_API_KEY", "OPENAI_API_KEY"),
    )
    temperature: float = 0.7
