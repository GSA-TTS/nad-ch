from typing import Optional
from nad_ch.application.dtos import DownloadResult
from nad_ch.domain.entities import DataProvider, DataSubmission
from nad_ch.domain.repositories import DataProviderRepository, DataSubmissionRepository


class FakeDataProviderRepository(DataProviderRepository):
    def __init__(self) -> None:
        self._providers = set()
        self._next_id = 1

    def add(self, provider: DataProvider) -> DataProvider:
        provider.id = self._next_id
        self._providers.add(provider)
        self._next_id += 1
        return provider

    def get_by_name(self, name: str) -> Optional[DataProvider]:
        return next((p for p in self._providers if p.name == name), None)

    def get_all(self):
        return sorted(list(self._providers), key=lambda provider: provider.id)


class FakeDataSubmissionRepository(DataSubmissionRepository):
    def __init__(self) -> None:
        self._submissions = set()
        self._next_id = 1

    def add(self, submission: DataSubmission) -> DataSubmission:
        submission.id = self._next_id
        self._submissions.add(submission)
        self._next_id += 1
        return submission

    def get_by_id(self, id: int) -> Optional[DataSubmission]:
        return next((s for s in self._submissions if s.id == id), None)

    def get_by_provider(self, provider: DataProvider) -> Optional[DataSubmission]:
        return [s for s in self._submissions if s.provider.name == provider.name]

    def get_by_filename(self, filename: str) -> Optional[DataSubmission]:
        return next((s for s in self._submissions if s.filename == filename), None)

    def update_report(self, submission_id: int, report) -> None:
        return None


class FakeStorage:
    def __init__(self):
        self._files = set()

    def upload(self, source: str, destination: str) -> bool:
        self._files.add(destination)
        return True

    def download_temp(self, filename: str) -> Optional[DownloadResult]:
        return DownloadResult(temp_dir=filename, extracted_dir=f"{filename}.gdb")

    def cleanup_temp_dir(self, temp_dir: str):
        pass


class MockCeleryTask:
    def __init__(self, result=None):
        self.result = result
        self.called = False

    def delay(self, *args, **kwargs):
        self.called = True
        return self

    def get(self, timeout=None, propagate=True, **kwargs):
        if self.result is None:
            raise Exception("No result has been set for the mock task")
        return self.result