# constants used by the new compconfig
import paramtools
from marshmallow import fields, Schema
from datetime import datetime
from taxbrain import TaxBrain


POLICY_SCHEMA = {
    "labels": {
        "year": {
            "type": "int",
            "validators": {
                "choice": {
                    "choices": [
                        yr
                        for yr in range(
                            TaxBrain.FIRST_BUDGET_YEAR,
                            TaxBrain.LAST_BUDGET_YEAR + 1,
                        )
                    ]
                }
            },
        },
        "MARS": {
            "type": "str",
            "validators": {
                "choice": {
                    "choices": [
                        "single",
                        "mjoint",
                        "mseparate",
                        "headhh",
                        "widow",
                    ]
                }
            },
        },
        "idedtype": {
            "type": "str",
            "validators": {
                "choice": {
                    "choices": [
                        "med",
                        "sltx",
                        "retx",
                        "cas",
                        "misc",
                        "int",
                        "char",
                    ]
                }
            },
        },
        "EIC": {
            "type": "str",
            "validators": {
                "choice": {"choices": ["0kids", "1kid", "2kids", "3+kids"]}
            },
        },
        "data_source": {
            "type": "str",
            "validators": {"choice": {"choices": ["PUF", "CPS", "other"]}},
        },
    },
    "additional_members": {
        "section_1": {"type": "str"},
        "section_2": {"type": "str"},
        "start_year": {"type": "int"},
        "checkbox": {"type": "bool"},
    },
}

AGG_ROW_NAMES = [
    "ind_tax",
    "payroll_tax",
    "combined_tax",
    "benefit_cost_total",
]

RESULTS_TABLE_TITLES = {
    "diff_comb_xbin": (
        "Combined Payroll and Individual Income Tax: Difference"
        " between Base and User plans by expanded income bin"
    ),
    "diff_comb_xdec": (
        "Combined Payroll and Individual Income Tax: Difference"
        " between Base and User plans by expanded income "
        "decile"
    ),
    "diff_itax_xbin": (
        "Individual Income Tax: Difference between Base and "
        "User plans by expanded income bin"
    ),
    "diff_itax_xdec": (
        "Individual Income Tax: Difference between Base and "
        "User plans by expanded income decile"
    ),
    "diff_ptax_xbin": (
        "Payroll Tax: Difference between Base and User plans "
        "by expanded income bin"
    ),
    "diff_ptax_xdec": (
        "Payroll Tax: Difference between Base and User plans "
        "by expanded income decile"
    ),
    "dist1_xbin": "Base plan tax vars, weighted total by expanded income bin",
    "dist1_xdec": (
        "Base plan tax vars, weighted total by expanded income " "decile"
    ),
    "dist2_xbin": "User plan tax vars, weighted total by expanded income bin",
    "dist2_xdec": (
        "User plan tax vars, weighted total by expanded income " "decile"
    ),
    "aggr_1": "Total Liabilities Baseline by Calendar Year (Billions)",
    "aggr_d": "Total Liabilities Change by Calendar Year (Billions)",
    "aggr_2": "Total Liabilities Reform by Calendar Year (Billions)",
}

RESULTS_TABLE_TAGS = {
    # diff tables
    "diff_comb_xbin": {
        "table_type": "diff",
        "tax_type": "combined",
        "grouping": "bins",
    },
    "diff_comb_xdec": {
        "table_type": "diff",
        "tax_type": "combined",
        "grouping": "deciles",
    },
    "diff_itax_xbin": {
        "table_type": "diff",
        "tax_type": "ind_income",
        "grouping": "bins",
    },
    "diff_itax_xdec": {
        "table_type": "diff",
        "tax_type": "ind_income",
        "grouping": "deciles",
    },
    "diff_ptax_xbin": {
        "table_type": "diff",
        "tax_type": "payroll",
        "grouping": "bins",
    },
    "diff_ptax_xdec": {
        "table_type": "diff",
        "tax_type": "payroll",
        "grouping": "deciles",
    },
    # dist tables
    "dist1_xbin": {"table_type": "dist", "law": "current", "grouping": "bins"},
    "dist1_xdec": {
        "table_type": "dist",
        "law": "current",
        "grouping": "deciles",
    },
    "dist2_xbin": {"table_type": "dist", "law": "reform", "grouping": "bins"},
    "dist2_xdec": {
        "table_type": "dist",
        "law": "reform",
        "grouping": "deciles",
    },
    # aggr tables
    "aggr_1": {"law": "current"},
    "aggr_d": {"law": "change"},
    "aggr_2": {"law": "reform"},
    # gdp elaticity model table
    "gdp_effect": {"default": "gdp_elast"},
}
RESULTS_TOTAL_ROW_KEY_LABELS = {
    "ind_tax": "Individual Income Tax Liability",
    "payroll_tax": "Payroll Tax Liability",
    "combined_tax": (
        "Combined Payroll and Individual Income Tax " + "Liability"
    ),
    "benefit_cost_total": "Total Benefits Spending",
}

MONEY_VARS = {
    "AGI",
    "Standard Deduction",
    "Itemized Deduction",
    "Personal Exemption",
    "Taxable Income",
    "Regular Tax",
    "AMTI",
    "Tax before Credits",
    "Non-refundable Credits",
    "Other Taxes",
    "Refundable Credits",
    "Individual Income Tax Liabilities",
    "Payroll Tax Liablities",
    "Combined Payroll and Individual Income Tax Liabilities",
    "Universal Basic Income",
    "Total Cost of Benefits",
    "Consumption Value of Benefits",
    "Expanded Income",
    "After-Tax Expanded Income",
    "Average Tax Change",
    "Total Tax Difference",
}


class MetaParameters(paramtools.Parameters):
    array_first = True
    defaults = {
        "year": {
            "title": "Start Year",
            "description": "Year for parameters.",
            "type": "int",
            "value": min(datetime.now().year, TaxBrain.LAST_BUDGET_YEAR),
            "validators": {
                "when": {
                    "param": "data_source",
                    "is": "CPS",
                    "then": {
                        "range": {
                            "min": 2014,
                            "max": TaxBrain.LAST_BUDGET_YEAR,
                        }
                    },
                    "otherwise": {
                        "range": {
                            "min": 2013,
                            "max": TaxBrain.LAST_BUDGET_YEAR,
                        }
                    },
                }
            },
        },
        "data_source": {
            "title": "Data Source",
            "description": "CPS is currently the only supported data source",
            "type": "str",
            "value": "CPS",
            "validators": {"choice": {"choices": ["CPS"]}},
        },
        "use_full_sample": {
            "title": "Use Full Sample",
            "description": "Use entire data set or a 2% sample.",
            "type": "bool",
            "value": True,
            "validators": {"choice": {"choices": [True, False]}},
        },
    }

    def dump(self, *args, **kwargs):
        """
        This method extends the default ParamTools dump method by swapping the
        when validator for a choice validator. This is required because C/S does
        not yet implement the when validator.
        """
        data = super().dump(*args, **kwargs)
        if self.data_source == "CPS":
            data["year"]["validators"] = {
                "choice": {
                    "choices": list(range(2014, TaxBrain.LAST_BUDGET_YEAR))
                }
            }
        else:
            data["year"]["validators"] = {
                "choice": {
                    "choices": list(range(2013, TaxBrain.LAST_BUDGET_YEAR))
                }
            }
        return data
