## Description
<!-- What does this PR do? Link to requirement/issue. -->
Closes #

## Type of Change
- [ ] New feature (implements a requirement)
- [ ] Bug fix (resolves a problem report)
- [ ] Refactoring (no functional change)
- [ ] Documentation update
- [ ] CI/CD change

## Linked Requirements
<!-- Which REQ-XXX items does this implement? -->
-

## Linked Risk Items
<!-- Does this change affect any RM-XXX risk mitigations? -->
-

---

## IEC 62304 Design Review Checklist

### Code Quality
- [ ] Code follows project coding standards
- [ ] No compiler warnings or linter errors
- [ ] Adequate error handling for all failure modes
- [ ] No hardcoded credentials or secrets

### Safety & Risk
- [ ] Safety-critical code paths are identified and documented
- [ ] Risk mitigations are not weakened by this change
- [ ] Input validation covers all boundary conditions
- [ ] Failure modes fail safe (not fail dangerous)

### Traceability
- [ ] All new code references the requirement it implements (REQ-XXX in docstrings)
- [ ] Test cases exist for all new/modified requirements
- [ ] Traceability links are maintained (issue -> code -> test)

### Testing
- [ ] Unit tests pass locally
- [ ] Integration tests pass locally
- [ ] Code coverage >= 80% for changed files
- [ ] Edge cases and error paths are tested
- [ ] Performance tests pass (if latency-critical)

### Documentation
- [ ] Docstrings updated for new/changed functions
- [ ] Architecture docs updated if design changed
- [ ] CHANGELOG.md updated
- [ ] API documentation updated (if applicable)

### SOUP/Dependencies
- [ ] No new unreviewed dependencies added
- [ ] Dependency versions are pinned
- [ ] License compatibility verified for new dependencies
- [ ] Security scan passes with no new HIGH/CRITICAL CVEs

---

## Reviewer Notes
<!-- Anything specific reviewers should focus on? -->

## Screenshots/Evidence
<!-- For UI changes or test evidence -->
