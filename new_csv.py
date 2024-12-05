import os
import json
import pandas as pd
import re

def extract_product_id(product_link):
    """
    Extract the product ID by removing the last three digits (color code).
    """
    try:
        return product_link.split("/")[-1].split(".")[1][:-3]
    except IndexError:
        return None


def extract_color_code(product_link):
    """
    Extract the last three digits (color code) from the product link.
    """
    try:
        return product_link.split("/")[-1].split(".")[1][-3:]
    except IndexError:
        return None


def clean_price(price):
    """
    Extract the numerical price value from the price field, skipping any prefixes.
    """
    match = re.search(r"Rs\.(\d+(\.\d{2})?)", price)
    return match.group(1) if match else ""


def split_category_hierarchy(hierarchy):
    """
    Split category hierarchy by '/' and exclude the last value.
    """
    return [value.strip() for value in hierarchy.split("/") if value][:-1]

product_img_idx = {}
product_fetched = []
def format_shopify_csv(product, gender):
    global product_img_idx
    """
    Format a single product dictionary into Shopify-compatible CSV rows.
    """
    rows = []
    product_unique = product.get("product_link", "").split("/")[-1].split(".")[1]
    # if product_unique != "0456163187": return rows
    if product_unique in product_fetched : return rows
    product_fetched.append(product_unique)
    product_id = extract_product_id(product.get("product_link", ""))
    color_code = extract_color_code(product.get("product_link", ""))
    if not product_id or not color_code:
        return rows  # Skip products without valid product IDs or color codes

    title = product.get("name", "")
    subcategory = product.get("subcategory", "")
    price = clean_price(product.get("price", ""))
    original_price = clean_price(product.get("original_price", "")) or price
    valid_image_urls = [url for url in product.get("image_urls", []) if not url.startswith("data:image")]
    category_tags = split_category_hierarchy(product.get("category_hierarichy", ""))
    type_filter = category_tags[len(category_tags) - 1] if len(category_tags) else ""
    tags = ", ".join(category_tags)
    if price != original_price:
        tags += ", Sale"

    # Initialize or reset image position tracker for this product
    if product_id not in product_img_idx:
        product_img_idx[product_id] = 1

    # Filter sizes for a specific store (example: Vega City)
    # sizes = []
    # for store in product.get("stores", []):
    #     if store.get("name", "") == "Vega City":
    #         sizes = store.get("sizes", [])
    #         break

    sizes = {}
    for store in product.get("stores", []):
        # print("********")
        # print(store)
        ss = store.get("sizes", [])
        for size in ss:
            # print(ss)
            sizeCode = size.get("sizeCode", "")
            if not sizeCode in sizes:
                sizes[sizeCode] = 0
                # print(f"new code added for {sizeCode}")
            sizes[sizeCode] += size.get("avaiQty", 0)
            # print(f"increased qty for {sizeCode} to {sizes[sizeCode]}")


    # for store in product.get("stores", []):
    #     name = store.get("name", "")
    #     ss = store.get("sizes", [])
    #     for size in ss:
    #         row = {
    #             "Handle": product_id,
    #             "Variant ID": color_code,
    #             "Store": name,
    #             "Size": size.get("sizeCode", ""),
    #             "Qty": size.get("avaiQty", 0)
    #         }
    #         rows.append(row)

    # return rows

    # if product_id != "0970818" or product_id != "0970818": return rows 
    # if sizes:
    #     for idx, size in enumerate(sizes):
    #         base_row = {
    #             "Handle": product_id,
    #             "Title": title if idx == 0 else "",
    #             "Body (HTML)": "",
    #             "Vendor": "H&M",
    #             "Product Category": "",
    #             "Type": type_filter,
    #             "Command": "REPLACE",
    #             "Tags": tags if idx == 0 else "",
    #             "Published": "TRUE" if idx == 0 else "",
    #             "Option1 Name": "Color",
    #             "Option1 Value": color_code,  # Specify color for all variants
    #             "Option2 Name": "Size",
    #             "Option2 Value": map_size(gender, type_filter, size.get("sizeCode", ""), size_legend_df),
    #             "Option3 Name": "",
    #             "Option3 Value": "",
    #             "Variant SKU": "",
    #             "Variant Grams": "",
    #             "Variant Inventory Tracker": "shopify",  # Set to "shopify"
    #             "Variant Inventory Qty": size.get("avaiQty", 0),
    #             "Variant Inventory Policy": "deny",  # Set to "deny"
    #             "Variant Fulfillment Service": "manual",  # Set to "manual"
    #             "Variant Price": price,  # Add price in all rows
    #             "Variant Compare At Price": original_price,
    #             "Variant Requires Shipping": "TRUE",
    #             "Variant Taxable": "",
    #             "Variant Barcode": "",
    #             "Image Src": valid_image_urls[idx] if idx < len(valid_image_urls) else "",
    #             "Image Position": product_img_idx[product_id] if idx < len(valid_image_urls) else "",
    #             "Image Alt Text": "",
    #             "Gift Card": "",
    #             "SEO Title": "",
    #             "SEO Description": "",
    #             "Google Shopping / Google Product Category": "",
    #             "Google Shopping / Gender": "",
    #             "Google Shopping / Age Group": "",
    #             "Google Shopping / MPN": "",
    #             "Google Shopping / AdWords Grouping": "",
    #             "Google Shopping / AdWords Labels": "",
    #             "Google Shopping / Condition": "",
    #             "Google Shopping / Custom Product": "",
    #             "Google Shopping / Custom Label 0": "",
    #             "Google Shopping / Custom Label 1": "",
    #             "Google Shopping / Custom Label 2": "",
    #             "Google Shopping / Custom Label 3": "",
    #             "Google Shopping / Custom Label 4": "",
    #             "Variant Image": valid_image_urls[0] if valid_image_urls else "",
    #             "Variant Weight Unit": "",
    #             "Variant Tax Code": "",
    #             "Cost per item": "",
    #             "Price / International": "",
    #             "Compare At Price / International": "",
    #             "Status": "active" if idx == 0 else "",
    #         }
    #         if idx < len(valid_image_urls): product_img_idx[product_id] += 1
    #         rows.append(base_row)

    if sizes:
        for idx, (code, qty) in enumerate(sizes.items()):
            base_row = {
                "Handle": product_id,
                "Title": title if idx == 0 else "",
                "Body (HTML)": "",
                "Vendor": "H&M",
                "Product Category": "",
                "Type": type_filter,
                "Command": "REPLACE",
                "Tags": tags if idx == 0 else "",
                "Published": "TRUE" if idx == 0 else "",
                "Option1 Name": "Color",
                "Option1 Value": color_code,  # Specify color for all variants
                "Option2 Name": "Size",
                "Option2 Value": map_size(gender, type_filter, code, size_legend_df),
                "Option3 Name": "",
                "Option3 Value": "",
                "Variant SKU": "",
                "Variant Grams": "",
                "Variant Inventory Tracker": "shopify",  # Set to "shopify"
                "Variant Inventory Qty": qty,
                "Variant Inventory Policy": "deny",  # Set to "deny"
                "Variant Fulfillment Service": "manual",  # Set to "manual"
                "Variant Price": price,  # Add price in all rows
                "Variant Compare At Price": original_price,
                "Variant Requires Shipping": "TRUE",
                "Variant Taxable": "",
                "Variant Barcode": "",
                "Image Src": valid_image_urls[idx] if idx < len(valid_image_urls) else "",
                "Image Position": product_img_idx[product_id] if idx < len(valid_image_urls) else "",
                "Image Alt Text": "",
                "Gift Card": "",
                "SEO Title": "",
                "SEO Description": "",
                "Google Shopping / Google Product Category": "",
                "Google Shopping / Gender": "",
                "Google Shopping / Age Group": "",
                "Google Shopping / MPN": "",
                "Google Shopping / AdWords Grouping": "",
                "Google Shopping / AdWords Labels": "",
                "Google Shopping / Condition": "",
                "Google Shopping / Custom Product": "",
                "Google Shopping / Custom Label 0": "",
                "Google Shopping / Custom Label 1": "",
                "Google Shopping / Custom Label 2": "",
                "Google Shopping / Custom Label 3": "",
                "Google Shopping / Custom Label 4": "",
                "Variant Image": valid_image_urls[0] if valid_image_urls else "",
                "Variant Weight Unit": "",
                "Variant Tax Code": "",
                "Cost per item": "",
                "Price / International": "",
                "Compare At Price / International": "",
                "Status": "active" if idx == 0 else "",
            }
            if idx < len(valid_image_urls): product_img_idx[product_id] += 1
            rows.append(base_row)

        # Add extra rows for remaining images
        for img_idx in range(len(sizes), len(valid_image_urls)):
            extra_row = {
                "Handle": product_id,
                "Command": "REPLACE",
                "Image Src": valid_image_urls[img_idx],
                "Image Position": product_img_idx[product_id],
            }
            product_img_idx[product_id] += 1
            rows.append(extra_row)

    return rows

import pandas as pd

def load_size_legend(file_path):
    """
    Load the size legend from a CSV file into a DataFrame,
    ensuring that H&M_code is treated as a string.
    """
    try:
        size_legend = pd.read_csv(file_path, dtype={"H&M_code": str})
        return size_legend
    except Exception as e:
        print(f"Error loading size legend file: {e}")
        return None

def map_size(gender, sub_category, hm_code, size_legend):
    """
    Map the H&M size code to the corresponding size using the size legend.
    Performs case-insensitive matching against all entries in the CSV.
    """
    try:
        # Ensure inputs are strings and convert to lowercase for case-insensitive matching
        gender = str(gender).lower()
        sub_category = str(sub_category).lower()
        hm_code = str(hm_code).lower()
        # print(f"gender {gender} sub_category {sub_category} code {hm_code}")
        # Convert relevant DataFrame columns to lowercase for case-insensitive matching
        filtered_legend = size_legend[
            (size_legend["Gender"].str.lower() == gender) &
            (size_legend["Sub_category"].str.lower() == sub_category) &
            (size_legend["H&M_code"].str.lower() == hm_code)
        ]
        
        # Return the corresponding Final_mapping value
        if not filtered_legend.empty:
            return filtered_legend.iloc[0]["FInal_mapping"]
        else:
            return hm_code
    except Exception as e:
        print(f"Error mapping size: {e}")
        return "Error"

def process_shopify_csv(json_file, csv_file, gender):
    """
    Process a single JSON file and convert it to Shopify-compatible CSV.
    """
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        all_rows = []
        for product in data:
            all_rows.extend(format_shopify_csv(product, gender))

        # Convert to DataFrame and save as CSV
        df = pd.DataFrame(all_rows)
        df.to_csv(csv_file, index=False, encoding="utf-8")
        print(f"Converted {json_file} to {csv_file}")
    except Exception as e:
        print(f"Error processing {json_file}: {e}")


def json_to_shopify_csv(directory, output_dir):
    """
    Process all `products.json` files in subfolders of a directory into Shopify-compatible CSVs.
    """
    os.makedirs(output_dir, exist_ok=True)

    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path):
            json_file = os.path.join(subdir_path, "products.json")
            gender = os.path.basename(directory)  # Determine gender from the main folder name

            if os.path.exists(json_file):
                csv_file = os.path.join(output_dir, f"{subdir}.csv")
                process_shopify_csv(json_file, csv_file, gender)
            else:
                print(f"products.json not found in {subdir_path}")

def csv_creater(who):

    directory = who  # Change to the appropriate folder
    csv_output_directory = f"csv_data_{who}_sizes_v4"

    if os.path.exists(directory):
        json_to_shopify_csv(directory, csv_output_directory)    

# Main execution
if __name__ == "__main__":
    size_legend_df = load_size_legend("mapping.csv")
    csv_creater("women")
    csv_creater("baby_girl")
    csv_creater("baby_boy")
    csv_creater("men")
    csv_creater("kids")