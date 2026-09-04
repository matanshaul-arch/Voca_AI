import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from voca_tse.app.service import LocalTSEService


def create_app(checkpoint: str, work_dir: str = "data/cache/local-prototype",
               ecapa_cache: str = "data/cache/ecapa-voxceleb") -> FastAPI:
    service = LocalTSEService(Path(checkpoint), Path(work_dir), Path(ecapa_cache))
    app = FastAPI(title="Voca AI Local Prototype")

    @app.get("/api/health")
    def health():
        return {"status": "ok", "local_only": True, "checkpoint": Path(checkpoint).name,
                "encoder_backend": service.backend, "lambda_level": service.lambda_level}

    @app.post("/api/profiles/preview")
    async def preview(enrollment: UploadFile = File(...)):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "enrollment"
            path.write_bytes(await enrollment.read())
            try:
                return service.preview(path)
            except Exception as exc:
                raise HTTPException(400, str(exc)) from exc

    @app.post("/api/separate")
    async def separate(enrollment: UploadFile = File(...), mixture: UploadFile = File(...)):
        with TemporaryDirectory() as directory:
            enrollment_path, mixture_path = Path(directory) / "enrollment", Path(directory) / "mixture"
            enrollment_path.write_bytes(await enrollment.read())
            mixture_path.write_bytes(await mixture.read())
            try:
                result = service.separate(enrollment_path, mixture_path)
            except Exception as exc:
                raise HTTPException(400, str(exc)) from exc
        return {"job_id": result.job_id, "audio_url": f"/api/jobs/{result.job_id}/audio",
                "duration_seconds": result.duration_seconds, "processing_seconds": result.processing_seconds,
                "realtime_factor": result.realtime_factor, "encoder_backend": result.encoder_backend,
                "lambda_level": result.lambda_level, "experimental": True}

    @app.get("/api/jobs/{job_id}/audio")
    def audio(job_id: str):
        path = service.work_dir / f"{job_id}.wav"
        if not path.is_file():
            raise HTTPException(404, "result not found")
        return FileResponse(path, media_type="audio/wav", filename="voca-separated.wav")

    @app.delete("/api/jobs/{job_id}")
    def delete(job_id: str):
        if not service.delete(job_id):
            raise HTTPException(404, "result not found")
        return {"deleted": True}
    static_dir = Path(__file__).parent / "static"
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    import uvicorn
    uvicorn.run(create_app(args.checkpoint), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
