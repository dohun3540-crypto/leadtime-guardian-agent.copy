# TEAM2_INTERFACE_REQUEST — operational Studio and Python boundary

To: Team 2 (Python engine / Studio Adapter owner). This is a technical handoff request, **not a request to change ownership**.

Please return for C001 first, then C013/C017/C008:

1. Latest original repository PR #12 HEAD Git SHA and CI URL; whether the engine/Adapter changed since `e9b9992b593a42d427ff1bbadeb9a9866ca593bd`.
2. Actual **saved** operational Studio Agent, Config ID, saved version, Step/Job IDs and timestamps. Distinguish user-supplied `studio.workflow-config-draft` v5 from real published/used job Config and from V4 archived C001.
3. Original unchanged operating Native JSON bytes + SHA-256, `studio-provenance/1` sidecar, Python input documents, execution status, output analysis JSON, validation issues and Git SHA. If output is a replay, label `ARCHIVED_REPLAY`, not new LIVE.
4. Operating job's actual PDF upload receipt: `{case_id,files:[{filename,file_id,sha256,hash_origin}]}`, complete 3-file set, SHA from original bytes, plus traceable job-file linkage. Actual independent QA Job uses different file IDs; compare original PDF SHA/case_id, not Job ID equality.
5. Confirm that untrusted Studio document inputs always pass `studio_integration.validate_documents`, not a bypass through `engine.analyze_portfolio`; clarify where document quantity/receipt/PO validation executes. Operative `studio_adapter.apply_studio_extractions` and `strict_json` versions should be documented.
6. Review v5 Extract schema: selected `po_id`/`supplier_id`/date descriptions permit null, but the schema declares only primitive types. Please fix under Studio ownership only after backing up Config and report before/after diff and actual saved Config/Job run.
7. Document the C008 R1=40/R2=60 receipt-level logic, C013 PO999 fail-closed, C017 Korean-date source-evidence handling. Return validated results including nulls/flags, not manually repaired predicted values.
8. Source-PDF verification status and Human Gold remain distinct; `evidence_verified_against_pdf=false` in a sidecar is not a defect and does not prove Python QA PASS.

Do not merge or change a running production workflow as part of this request. Provide explicit UNAVAILABLE/BLOCKED for missing files.
