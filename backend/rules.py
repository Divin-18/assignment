class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3
    WHITE = 4

def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index):
    pnl = data.get("financials")[financial_index].get("lineItems", {}).get("pnl", {})
    return pnl.get("netRevenue", 0)

def total_borrowing(data: dict, financial_index):
    bs = data.get("financials")[financial_index].get("balanceSheet", {})
    total_borrowings = bs.get("longTermBorrowings", 0) + bs.get("shortTermBorrowings", 0)
    total_revenue_value = total_revenue(data, financial_index)

    return total_borrowings / total_revenue_value if total_revenue_value != 0 else 0

def iscr(data: dict, financial_index):
    pnl = data.get("financials")[financial_index].get("lineItems", {}).get("pnl", {})
    bs = data.get("financials")[financial_index].get("balanceSheet", {})

    profit_before_interest_tax_depreciation = pnl.get("profitBeforeInterestTaxDepreciation", 0)
    interest_expenses = bs.get("interestExpenses", 0)

    return (profit_before_interest_tax_depreciation + 1) / (interest_expenses + 1) if interest_expenses != 0 else 0

def iscr_flag(data: dict, financial_index):
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index):
    total_revenue_value = total_revenue(data, financial_index)
    return FLAGS.GREEN if total_revenue_value >= 50000000 else FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index):
    borrowing_to_revenue_ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if borrowing_to_revenue_ratio <= 0.25 else FLAGS.AMBER
