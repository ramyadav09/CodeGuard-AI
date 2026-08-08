import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DiffChunk(BaseModel):
    old_start: int
    old_lines: int
    new_start: int
    new_lines: int
    header: str
    content: str
    added_lines: List[Dict[str, Any]] = Field(default_factory=list) # [{"line_no": 42, "code": "def foo():"}]


class FileDiff(BaseModel):
    file_path: str
    old_path: Optional[str] = None
    new_path: Optional[str] = None
    status: str = "modified" # added, modified, deleted, renamed
    chunks: List[DiffChunk] = Field(default_factory=list)
    raw_patch: str = ""
    additions_count: int = 0
    deletions_count: int = 0


class ParsedDiff(BaseModel):
    files: List[FileDiff] = Field(default_factory=list)
    total_files: int = 0
    total_additions: int = 0
    total_deletions: int = 0


class DiffParser:
    @staticmethod
    def parse_patch(raw_diff: str) -> ParsedDiff:
        if not raw_diff or not raw_diff.strip():
            return ParsedDiff()

        files: List[FileDiff] = []
        raw_file_diffs = raw_diff.split("diff --git ")

        for raw_file in raw_file_diffs:
            if not raw_file.strip():
                continue

            lines = raw_file.split("\n")
            header_line = lines[0] # e.g. "a/src/main.py b/src/main.py"
            
            # Extract file path
            path_match = re.search(r"b/(.+)$", header_line)
            file_path = path_match.group(1) if path_match else "unknown"

            status = "modified"
            old_path = None
            new_path = file_path

            for line in lines[1:10]:
                if line.startswith("new file mode"):
                    status = "added"
                elif line.startswith("deleted file mode"):
                    status = "deleted"
                elif line.startswith("--- a/"):
                    old_path = line[6:]
                elif line.startswith("+++ b/"):
                    new_path = line[6:]

            # Parse chunks
            chunks: List[DiffChunk] = []
            current_chunk: Optional[DiffChunk] = None
            chunk_lines: List[str] = []
            additions = 0
            deletions = 0
            current_new_line = 0

            for line in lines:
                if line.startswith("@@ "):
                    if current_chunk:
                        current_chunk.content = "\n".join(chunk_lines)
                        chunks.append(current_chunk)
                        chunk_lines = []

                    # Parse @@ -old_start,old_lines +new_start,new_lines @@
                    chunk_match = re.search(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)", line)
                    if chunk_match:
                        old_start = int(chunk_match.group(1))
                        old_lines = int(chunk_match.group(2)) if chunk_match.group(2) else 1
                        new_start = int(chunk_match.group(3))
                        new_lines = int(chunk_match.group(4)) if chunk_match.group(4) else 1
                        header = line

                        current_chunk = DiffChunk(
                            old_start=old_start,
                            old_lines=old_lines,
                            new_start=new_start,
                            new_lines=new_lines,
                            header=header,
                            content=""
                        )
                        current_new_line = new_start
                elif current_chunk:
                    chunk_lines.append(line)
                    if line.startswith("+") and not line.startswith("+++"):
                        additions += 1
                        current_chunk.added_lines.append({
                            "line_no": current_new_line,
                            "code": line[1:]
                        })
                        current_new_line += 1
                    elif line.startswith("-") and not line.startswith("---"):
                        deletions += 1
                    elif not line.startswith("\\"):
                        current_new_line += 1

            if current_chunk:
                current_chunk.content = "\n".join(chunk_lines)
                chunks.append(current_chunk)

            file_diff = FileDiff(
                file_path=new_path or file_path,
                old_path=old_path,
                new_path=new_path,
                status=status,
                chunks=chunks,
                raw_patch=raw_file,
                additions_count=additions,
                deletions_count=deletions
            )
            files.append(file_diff)

        total_additions = sum(f.additions_count for f in files)
        total_deletions = sum(f.deletions_count for f in files)

        return ParsedDiff(
            files=files,
            total_files=len(files),
            total_additions=total_additions,
            total_deletions=total_deletions
        )
