soc case report

**Severity:** critical
**Score:** 85/100

## Alerts
- `A-1001` 2026-04-08T10:12:00Z from EDR **A-1001**: Suspicious outbound connection to https://evil-example.com/path from host WS-77
- `A-1002` 2026-04-08T10:20:00Z from DNS **A-1002**: Multiple queries for bad-domain.test and 8.8.8.8 observed
- `A-1003` 2026-04-08T10:35:00Z from Email **A-1003**: Attachment hash 44d88612fea8a8f36de82e1278abb02f seen in message

## IOCs
| Type | Value | Normalized |
|------|-------|------------|
| domain | evil-example.com | evil-example.com |
| url | https://evil-example.com/path | https://evil-example.com/path |
| ip | 8.8.8.8 | 8.8.8.8 |
| domain | bad-domain.test | bad-domain.test |
| hash | 44d88612fea8a8f36de82e1278abb02f | 44d88612fea8a8f36de82e1278abb02f |

## Enrichments
| Vendor | IOC | Verdict | Confidence | Details |
|--------|-----|---------|------------|---------|
| mock-ti | evil-example.com | benign | 10 | {'sha256_prefix': '58a17dd3'} |
| mock-ti | https://evil-example.com/path | malicious | 90 | {'sha256_prefix': '5eb86260'} |
| mock-ti | 8.8.8.8 | unknown | 50 | {'sha256_prefix': '838c4c25'} |
| mock-ti | bad-domain.test | unknown | 50 | {'sha256_prefix': '8753146f'} |
| mock-ti | 44d88612fea8a8f36de82e1278abb02f | unknown | 50 | {'sha256_prefix': '1f2b9e9e'} |

## Recommendations
- Escalate immediately to the incident response team.
- Contain affected hosts and block confirmed indicators.