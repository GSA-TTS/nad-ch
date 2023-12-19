from typing import List
from nad_ch.application_context import ApplicationContext
from nad_ch.domain.entities import DataProvider, DataSubmission


def add_data_provider(
      ctx: ApplicationContext, provider_name: str
) -> None:
    if not provider_name:
        ctx.logger.error('Provider name required')
        return

    matching_provider = ctx.providers.get_by_name(provider_name)
    if matching_provider:
        ctx.logger.error('Provider name must be unique')
        return

    provider = DataProvider(provider_name)
    ctx.providers.add(provider)
    ctx.logger.info('Provider added')


def list_data_providers(ctx: ApplicationContext) -> List[DataProvider]:
    providers = ctx.providers.get_all()
    ctx.logger.info('Data Provider Names:')
    for p in providers:
        ctx.logger.info(p.name)

    return providers


def ingest_data_submission(
        ctx: ApplicationContext, file_name: str, provider_name: str
) -> None:
    if not file_name:
        ctx.logger.error('File name required')
        return

    provider = ctx.providers.get_by_name(provider_name)
    if not provider:
        ctx.logger.error('Provider with that name does not exist')
        return

    ctx.storage.upload(file_name, f'{provider.name}_{file_name}')
    url = ctx.storage.get_file_url(file_name)

    submission = DataSubmission(file_name, url, provider)
    ctx.submissions.add(submission)
    ctx.logger.info('Submission added')


def list_data_submissions_by_provider(
        ctx: ApplicationContext, provider_name: str
) -> List[DataSubmission]:
    provider = ctx.providers.get_by_name(provider_name)
    if not provider:
        ctx.logger.error('Provider with that name does not exist')
        return

    submissions = ctx.submissions.get_by_provider(provider)
    ctx.logger.info(f'Data submissions for {provider.name}')
    for s in submissions:
        ctx.logger.info(f'{s.provider.name}: {s.file_name}')

    return submissions
