from os import name
from typing import Mapping
from pydantic import BaseModel, Field, field_validator
from dify_plugin.tool.entities import ProviderConfig

from dify_plugin.utils.yaml_loader import load_yaml_file


class EndpointConfigurationExtra(BaseModel):
    class Python(BaseModel):
        source: str

    python: Python

class EndpointConfiguration(BaseModel):
    path: str
    method: str
    extra: EndpointConfigurationExtra

class EndpointProviderConfiguration(BaseModel):
    settings: Mapping[str, ProviderConfig] = Field(default_factory=dict)
    endpoints: list[EndpointConfiguration] = Field(default_factory=list)

    @field_validator("endpoints", mode="before")
    def validate_endpoints(cls, value) -> list[EndpointConfiguration]:
        if not isinstance(value, list):
            raise ValueError("endpoints should be a list")

        endpoints: list[EndpointConfiguration] = []

        for endpoint in value:
            # read from yaml
            if not isinstance(endpoint, str):
                raise ValueError("endpoint path should be a string")
            try:
                file = load_yaml_file(endpoint)
                endpoints.append(EndpointConfiguration(**file))
            except Exception as e:
                raise ValueError(f"Error loading endpoint configuration: {str(e)}")

        return endpoints

    @field_validator("settings", mode="before")
    def validate_settings(cls, value: dict[str, dict]) -> Mapping[str, dict]:
        if not isinstance(value, dict):
            raise ValueError("settings should be a dict")
        
        # add name field for each provider config
        for key, v in value.items():
            v['name'] = key
        
        return value