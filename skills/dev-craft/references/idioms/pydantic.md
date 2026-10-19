# Pydantic

Detect v1 vs v2 in the lockfile; this file assumes v2. Never mix v1 patterns into a v2 repo.
- `model_config = ConfigDict(...)`, `field_validator` / `model_validator`, `model_dump()` / `model_validate()`.
- Settings via `pydantic-settings` (`BaseSettings` lives there in v2); env-driven, typed, no secrets in code.
- Separate input, output and DB models (`UserCreate`, `UserRead`); use `from_attributes=True` for ORM reads.
- Constrain fields (`Field(min_length=..., ge=...)`), use `Decimal` for money, aware datetimes.
- Traps: v1 `class Config`, `.dict()`, `@validator`; `Optional` fields without a default; leaking secrets in `repr`
  (use `SecretStr`).
