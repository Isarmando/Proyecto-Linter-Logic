from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from github import Github
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Auditor de Código con IA",
    description="Backend del sistema de auditoría de código inteligente",
    version="0.1"
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class RepoRequest(BaseModel):
    github_url: str

@app.get("/")
def root():
    return {
        "message": "Backend funcionando correctamente",
        "service": "Auditor de Código con IA"
    }

@app.post("/analizar")
def analizar_repositorio(request: RepoRequest):
    try:
        # Extraer usuario/repositorio de la URL
        partes = request.github_url.rstrip("/").split("/")
        usuario = partes[-2]
        repo_nombre = partes[-1]

        # Conectar a GitHub
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(f"{usuario}/{repo_nombre}")

        # Obtener lista de archivos
        archivos = []
        contenidos = repo.get_contents("")
        while contenidos:
            archivo = contenidos.pop(0)
            if archivo.type == "dir":
                contenidos.extend(repo.get_contents(archivo.path))
            else:
                archivos.append(archivo.path)

        return {
            "repositorio": repo.full_name,
            "archivos": archivos,
            "total": len(archivos)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))