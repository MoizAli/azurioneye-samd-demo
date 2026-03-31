"""
Configuration management (12-factor app principles).

Safety-Critical Parameters:
  - audit_log_enabled: Must always be True for medical device
  - max_latency_ms: Class B performance requirement (REQ-005)
  - clinical_validation_strict: Always True, no bypass

Design Reference: SDDD Section 1.3 - Configuration Management
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str = "AzurionEye AI Operator"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False
    port: int = 8000

    # Database
    database_url: str = "postgresql://user:pass@localhost/azurioneye"

    # Logging (safety-critical, REQ-002)
    log_level: str = "INFO"
    audit_log_enabled: bool = True

    # Performance (Class B requirement, REQ-005)
    max_latency_ms: int = 500

    # Clinical data validation (safety-critical)
    clinical_validation_strict: bool = True

    # ML Model
    model_path: str = "src/azurioneye_operator/models/v1.0.0"
    model_version: str = "1.0.0"

    # Security
    require_https: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
