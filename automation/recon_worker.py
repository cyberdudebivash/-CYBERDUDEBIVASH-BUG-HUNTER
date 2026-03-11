from analysis.ai_recon_analyzer import AIReconAnalyzer

analyzer = AIReconAnalyzer()


async def run_recon_worker(domain, program):

    pipeline = ReconPipeline(domain)

    results = await pipeline.run()

    analysis = await analyzer.analyze(domain, results)

    print("[AI ANALYSIS]", analysis)

    return results