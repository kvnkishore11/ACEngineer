# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml", "rich"]
# ///

"""List brands, products, trees, branches, and leaves for ui-agents."""

import sys
from pathlib import Path
import yaml
from rich.console import Console
from rich.table import Table

APPS_DIR = Path(__file__).parent.parent / "apps" / "infinite-ui" / "src" / "brands"
console = Console()


STATUS_ICONS = {
    "validated": "[green]✓[/green]",
    "generating": "[yellow]●[/yellow]",
    "validating": "[yellow]●[/yellow]",
    "draft": "[dim]○[/dim]",
    "failed": "[red]✗[/red]",
}


def list_brands():
    brands = sorted(
        d.name for d in APPS_DIR.iterdir()
        if d.is_dir() and d.name != "_template"
    )
    table = Table(title="Brands")
    table.add_column("Name")
    for b in brands:
        table.add_row(b)
    console.print(table)


def list_products(brand: str):
    brand_dir = APPS_DIR / brand
    if not brand_dir.exists():
        console.print(f"[red]Brand '{brand}' not found[/red]")
        sys.exit(1)
    products_dir = brand_dir / "products"
    if not products_dir.exists():
        console.print(f"[yellow]No products directory for brand '{brand}'[/yellow]")
        return
    products = sorted(
        d.name for d in products_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )
    table = Table(title=f"Brand: {brand}")
    table.add_column("Product")
    table.add_column("Notes")
    for p in products:
        product_brand_yaml = products_dir / p / "brand.yaml"
        note = "has brand.yaml override" if product_brand_yaml.exists() else "inherits brand identity"
        table.add_row(p, note)
    console.print(table)


def load_manifest(brand: str, product: str):
    manifest_path = APPS_DIR / brand / "products" / product / "trees.yaml"
    if not manifest_path.exists():
        console.print(f"[red]No trees.yaml found for brand '{brand}', product '{product}'[/red]")
        sys.exit(1)
    with open(manifest_path) as f:
        return yaml.safe_load(f)


def list_trees(brand: str, product: str):
    manifest = load_manifest(brand, product)
    table = Table(title=f"Brand: {brand} | Product: {product}")
    table.add_column("Tree")
    table.add_column("Description")
    table.add_column("Branches", justify="right")
    for tree in manifest.get("trees", []):
        table.add_row(tree["slug"], tree["description"], str(len(tree.get("branches", []))))
    console.print(table)


def list_branches(brand: str, product: str, tree_slug: str):
    manifest = load_manifest(brand, product)
    tree = next((t for t in manifest.get("trees", []) if t["slug"] == tree_slug), None)
    if not tree:
        console.print(f"[red]Tree '{tree_slug}' not found in brand '{brand}', product '{product}'[/red]")
        sys.exit(1)
    table = Table(title=f"{brand}/{product} → {tree_slug}")
    table.add_column("Branch")
    table.add_column("Description")
    table.add_column("Status")
    table.add_column("Created")
    for b in tree.get("branches", []):
        icon = STATUS_ICONS.get(b["status"], "?")
        table.add_row(b["slug"], b["description"], f'{icon} {b["status"]}', b["created"])
    console.print(table)


def list_leaves(brand: str, product: str, tree_slug: str = ""):
    manifest = load_manifest(brand, product)
    trees_dir = APPS_DIR / brand / "products" / product / "trees"
    table = Table(title=f"Leaves: {brand}/{product}" + (f" → {tree_slug}" if tree_slug else ""))
    table.add_column("Path")
    table.add_column("Status")
    table.add_column("Exists")
    trees = manifest.get("trees", [])
    if tree_slug:
        trees = [t for t in trees if t["slug"] == tree_slug]
    for tree in trees:
        for b in tree.get("branches", []):
            leaf_path = trees_dir / tree["slug"] / b["slug"] / "index.vue"
            icon = STATUS_ICONS.get(b["status"], "?")
            exists = "[green]✓[/green]" if leaf_path.exists() else "[red]✗ missing[/red]"
            table.add_row(
                f'{tree["slug"]}/{b["slug"]}/index.vue',
                f'{icon} {b["status"]}',
                exists,
            )
    console.print(table)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] not in ("brands", "products", "trees", "branches", "leaves"):
        console.print("Usage: list.py {brands|products|trees|branches|leaves} [brand] [product] [tree]")
        sys.exit(1)
    cmd = args[0]
    if cmd == "brands":
        list_brands()
    elif cmd == "products":
        list_products(args[1])
    elif cmd == "trees":
        list_trees(args[1], args[2])
    elif cmd == "branches":
        list_branches(args[1], args[2], args[3])
    elif cmd == "leaves":
        list_leaves(args[1], args[2], args[3] if len(args) > 3 else "")
