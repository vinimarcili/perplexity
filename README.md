# Perplexity

## Configuração do Ollama (WSL + Windows)

Este projeto roda no WSL mas utiliza o Ollama instalado no Windows para ter acesso direto à GPU.

### 1. Instale o Ollama no Windows

Baixe e instale em [ollama.com](https://ollama.com).

### 2. Descubra o IP do host Windows dentro do WSL

```bash
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
```

### 3. Configure o `.env`

Crie um arquivo `.env` na raiz do projeto com o IP obtido:

```env
OLLAMA_WINDOWS_URL=http://<IP_DO_HOST>:11434
```

### 4. Libere o acesso no firewall do Windows (se necessário)

No PowerShell como administrador:

```powershell
netsh advfirewall firewall add rule name="Ollama" dir=in action=allow protocol=TCP localport=11434
```

### 5. Configure o Ollama para escutar em todas as interfaces

Defina a variável de ambiente no Windows:

```env
OLLAMA_HOST=0.0.0.0
```

Reinicie o Ollama após essa alteração.
