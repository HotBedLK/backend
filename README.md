# HotBed.lk Api Interface

## Supabase configuration

Set these environment variables (for example via `.env` or your deployment system):

```
SUPABASE_URL=your-project-url
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
# or use SUPABASE_ANON_KEY if you only need anon access
```

Use the shared client from any service:

```python
from app.database import get_supabase_client

supabase = get_supabase_client()
```
