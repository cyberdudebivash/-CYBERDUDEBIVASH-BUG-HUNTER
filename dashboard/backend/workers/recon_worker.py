from core.recon_pipeline import ReconPipeline


async def run_recon(domain):

    pipeline = ReconPipeline(domain)

    results = await pipeline.run()

    return results