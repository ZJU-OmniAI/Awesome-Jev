# Resource catalog

`resources.json` is the source of truth for the tables in both READMEs. Each entry records a stable ID, one of the three tracks, resource kind, evidence label, primary URL, and an original summary and limitation in English and Chinese.

`reviewed_on` records the editorial review date. It is not the paper's publication date or a claim of independent replication. `source_snapshot` identifies the documentation/code snapshot behind a summary. Live pages can change after that snapshot.

Evidence labels:

| Label | Meaning |
| --- | --- |
| `official` | Vendor documentation or vendor-reported results |
| `paper` | A paper or preprint; results are author-reported |
| `project` | Public implementation and project documentation |
| `demo` | Demonstration or small development run |
| `proposal` | A design proposal without a completed evaluation |
| `background` | Related work; not evidence of a Jev integration |

An entry may carry multiple labels. Inclusion is not endorsement or a performance ranking. This catalog does not claim that every linked project is reproducible from its public code.

After an edit, run from the repository root:

```bash
python3 scripts/update_catalog.py
python3 scripts/check_repository.py
```

## Demonstration records / 演示记录

[demo-records.json](demo-records.json) contains transcribed question and response examples for text and image inputs. Each record identifies its model, date, public image reference where available, candidates, and reported response fields. Five paired examples from *The Kid* belong to the same ten-question image call and should not be counted as independent runs.

The transcriptions have no complete original HTTP logs or independent ground-truth annotations. They explain interface behavior and candidate design, rather than establish benchmark accuracy. Request excerpts may omit image assets and are not directly executable payloads. The bottle-question definitions come from the linked Visual Jev public example.

该文件记录文本与图像示例的问题、候选和响应，并保留模型版本、日期及公开图像来源。《寻子遇仙记》的五组对照属于同一次十题请求，不是五次独立运行。记录用于分析候选设计；缺少完整 HTTP 日志和独立真值标注，不构成基准成绩，也不是可直接提交的完整请求。
