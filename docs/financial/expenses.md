# Handling Expenses

This page provides detailed procedures for handling ward expense reimbursements through the LCR Expenses system, including best practices to prevent common audit exceptions.

## Overview

Ward financial clerks are responsible for processing expense reimbursements for approved ward expenses. While the LCR Expenses system provides workflow automation, clerks must manually verify compliance with Church financial policies because the system has known limitations.

## The LCR Expenses System: Critical Flaws

!!! danger "Known System Limitations 🚨"
    **The LCR Expenses system has significant flaws that create audit risks:**

    1. **Permits self-approvals** - The system allows bishopric members to approve their own reimbursements
    2. **Doesn't enforce two-approval rule** - System may show "approved" with only one signature
    3. **Doesn't enforce documentation** - Expenses can be approved without attached receipts
    4. **No duplicate detection** - System won't warn of duplicate reimbursements

    **Church software developers are aware of these issues.** Until fixed, clerks are the final line of defense.

## Expense Approval Requirements

Every expense reimbursement MUST meet all these criteria:

| Requirement | Details | Why It Matters |
|-------------|---------|----------------|
| **Two Approvals** | Two members of bishopric must approve | Prevents fraud and errors |
| **Payee Cannot Approve** | Payee cannot be one of the two approvers | Eliminates conflict of interest |
| **Legible Receipt** | Receipt must show clear line items and sales tax | Proves proper use of funds |
| **Completed Form** | Reimbursement form fully filled out | Documents purpose and authorization |
| **No Duplicates** | Cross-check against recent reimbursements | Prevents accidental double-payment |

## Step-by-Step Processing Procedure

### Step 1: Receive Expense Request

When an expense request comes in through LCR:

1. **Open the request** in LCR Expenses module

2. **Note the requester name** and amount

3. **Check submission date** (should be timely, not months old)

### Step 2: Verify Documentation

Before looking at approvals, verify the documentation:

```markdown
Documentation Checklist:
☐ Receipt image attached
☐ Receipt is legible (can read all line items)
☐ Sales tax clearly shown
☐ Reimbursement form completed
☐ Purpose stated clearly
☐ Amount on receipt matches request amount
```

!!! warning "If Documentation is Missing or Illegible"
    **DO NOT PROCESS** the reimbursement. Instead:

    1. Return the request to the payee
    2. Request legible receipt or missing documentation
    3. Add comment in LCR explaining what's needed
    4. Set status to "Needs Information"

### Step 3: Verify Approvals

Check that two proper approvals are present:

1. **Count the approvals** - Must be exactly two

2. **Check the names** - Both must be bishopric members

3. **Verify payee exclusion** - Payee's name cannot be an approver

Example approval check:

| Payee | Approver 1 | Approver 2 | Valid? |
|-------|------------|------------|--------|
| Brother Smith | Bishop Jones | Brother Smith | ❌ NO - Payee is approver |
| Sister Garcia | Bishop Jones | 1st Counselor Lee | ✅ YES - Two proper approvals |
| Bishop Jones | 1st Counselor Lee | 2nd Counselor Chen | ✅ YES - Payee not approving |
| Brother Thompson | Bishop Jones | (none) | ❌ NO - Only one approval |

!!! tip "Fixing Approval Issues"
    If approvals are wrong:

    - **Missing approval**: Send to appropriate person for second signature
    - **Self-approval**: Return to payee, explain policy, get proper approvals
    - **Wrong approver**: Return and request bishopric member approval

    **Remember**: You can fix approval issues after the fact. Better to correct than to process incorrectly.

### Step 4: Check for Duplicates

Before final processing, verify this isn't a duplicate:

1. **Search recent reimbursements** for same payee (last 2 months)

2. **Compare amounts** - Is there an identical or very similar amount?

3. **Check dates** - Does the receipt date match a previous reimbursement?

4. **Review purpose** - Is it possibly the same expense submitted twice?

!!! danger "Duplicate Reimbursement Prevention"
    Duplicate reimbursements are a **common audit finding**. Take time to verify. If unsure:

    - Contact the payee directly
    - Ask: "I see a similar expense from [date]. Is this the same or different?"
    - Document the answer in LCR comments
    - Better safe than sorry!

### Step 5: Process or Return

Once verification is complete:

**If all requirements met:**

1. Add comment in LCR: "Verified: documentation complete, two proper approvals, no duplicate"

2. Mark as "Approved for Payment"

3. Payment will be processed in next check run

**If any issues found:**

1. Set status to "Needs Information" or "Returned"

2. Add detailed comment explaining exactly what's needed

3. Notify payee (LCR should email automatically, but confirm)

4. Track for follow-up

## Special Situations

### Cash Advances and Gift Cards

!!! warning "Special Rules Apply ⚠️"
    Cash advances (including gift cards) require extra controls:

    **Distribution Requirements:**
    - Two people must receive the check or gift card together
    - Document names of both recipients

    **Spending Requirements:**
    - Two people must oversee the spending
    - All expenditures documented with receipts
    - Any remaining funds must be returned

    **Settlement:**
    - Advance must be "settled" with receipts within 30 days
    - Cannot issue new advance if previous one unsettled

### Donations Incorrectly Submitted as Expenses

Sometimes members mistakenly submit donations through expenses:

!!! info "Donation vs. Expense"
    **Donations require donation slips**, not expense forms.

    If you see:
    - Contribution to missionary fund
    - Donation to humanitarian aid
    - Fast offering payment

    **Action**: Return the expense request and direct member to make proper donation with slip.

### Online Activity Registrations

When activity coordinators pay online with personal cards:

1. **Receipt must show**: Online confirmation, amount, activity name

2. **Documentation**: Screenshot of registration confirmation acceptable

3. **Timing**: Should be submitted soon after activity (not months later)

4. **Budget check**: Verify activity has budget available

## Handling Donation Slips

Related to expense processing, proper donation handling:

### Donation Requirements

!!! warning "All Donations Require a Slip"
    **NO EXCEPTIONS**. Every donation must have a completed, signed donation slip.

### Donation Discrepancy Procedure

**If donation amount doesn't match what's written on the slip:**

1. **DO NOT deposit the donation**

2. Give the donation to the bishop to hold securely

3. Contact the member to resolve the discrepancy

4. Once resolved, deposit and record correct amount

5. Document the resolution in clerk notes

### Activity Donations (Camps, Trek, etc.)

Members often donate for camps, Trek, or activities:

**Online Donations:**

- System allocates to "General Offerings" by default

- **Clerk must manually move** to appropriate activity account in LCR

- Don't wait - reallocate immediately after reconciliation

**Check Donations:**

- Must have accompanying donation slip

- Member must sign slip

- Slip should designate "General Offerings" (to be reallocated)

- Memo line can note "For Girls Camp" for reference

- Clerk reallocates after recording

## Monthly Best Practices

### Weekly Review

Don't let expenses pile up. Review at least weekly:

- Process new submissions within 2-3 days

- Follow up on pending items

- Clear out old "Needs Information" requests

### Monthly Bishop Review

During monthly financial review meeting:

- Show bishop summary of expense activity

- Flag any unusual patterns or concerns

- Verify all reimbursements were appropriate

- Discuss any policy questions

### Audit Preparation

Keep yourself audit-ready:

- All receipts legible and complete

- All approvals proper (can be fixed retroactively if needed)

- No duplicates

- Purpose documented

- No old unsettled advances

## Common Audit Exceptions and Prevention

| Audit Finding | Prevention |
|---------------|------------|
| Missing receipts | Verify before approving, return if missing |
| Illegible receipts | Require clear scans, reject blurry photos |
| Self-approvals | Check payee vs. approvers, return if match |
| Missing second approval | Count approvals, require two |
| Duplicate payments | Cross-check recent reimbursements |
| Unsettled advances | Track advances, follow up on settlements |
| Missing donation slips | Never accept cash/check without slip |

## Resources and Links

- [Church Handbook - Chapter 34.7: Reimbursements](https://www.churchofjesuschrist.org/study/manual/general-handbook/34-finances-and-audits#title_number21)

- [LCR Expenses Module](https://lcr.churchofjesuschrist.org/)

- [Financial Audits](audits.md) - Audit preparation guidance

- [Budgets](budgets.md) - Budget management procedures

---

## Quick Reference Card

Print this for your desk:

```
EXPENSE APPROVAL CHECKLIST
--------------------------
☐ Legible receipt with line items and tax
☐ Reimbursement form completed
☐ TWO proper approvals
☐ Payee is NOT an approver
☐ No duplicate in last 2 months
☐ Amount matches receipt
☐ Purpose clear and appropriate
☐ Budget available

CASH ADVANCE RULES
------------------
☐ Two people receive
☐ Two people oversee spending
☐ All receipts documented
☐ Remaining funds returned
☐ Settled within 30 days

DONATION RULES
--------------
☐ Every donation needs slip
☐ Member must sign slip
☐ If amount ≠ slip, HOLD and call member
☐ Online donations → move to activity account
☐ Check donations → get slip first
```

*Questions? Contact your stake financial clerk or refer to Church Handbook Chapter 34.*
