from .app import load_adzuna_jobs_per_skill
import azure.functions as func


def main(inBlob: func.InputStream):
    load_adzuna_jobs_per_skill(inBlob)
