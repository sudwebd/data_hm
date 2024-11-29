from imports_common import *

if __name__ == "__main__":
    # Step 1: Scrape main category and subcategories
    scrape_hnm_category("women", [4])

    # Step 2: Scrape products in parallel
    scrape_hnm_categories_parallel("women")