import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.brand import Brand
from src.product import Product
from database import Base

engine = create_engine("sqlite:///shoe_wear.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    return SessionLocal()

@click.group()
def cli():
    """ShoeWear Inventory Management System"""
    pass

@cli.group()
def brand():
    """Manage brands"""
    pass

@brand.command()
@click.option("--name", prompt="Brand name", help="Name of the brand")
@click.option("--description", prompt="Description (optional)", default="", help="Description of the brand")
def add(name, description):
    """Add a new brand"""
    db = get_session()
    try:
        brand = Brand.create(db, name, description or None)
        click.echo(f"Brand '{brand.name}' added successfully with ID: {brand.id}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)
    finally:
        db.close()

@brand.command()
def list():
    """List all brands"""
    db = get_session()
    brands = Brand.get_all(db)
    if not brands:
        click.echo("No brands found.")
        return
    
    click.echo("ID\tName\tDescription")
    click.echo("--\t----\t-----------")
    for brand in brands:
        click.echo(f"{brand.id}\t{brand.name}\t{brand.description or 'N/A'}")
    db.close()

@brand.command()
@click.argument("brand_id", type=int)
def delete(brand_id):
    """Delete a brand by ID"""
    db = get_session()
    brand = Brand.find_by_id(db, brand_id)
    if not brand:
        click.echo(f"Brand with ID {brand_id} not found.", err=True)
        return
    
    try:
        brand.delete(db)
        click.echo(f"Brand '{brand.name}' deleted successfully.")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)
    finally:
        db.close()

@brand.command()
@click.argument("brand_id", type=int)
def products(brand_id):
    """List all products for a brand"""
    db = get_session()
    brand = Brand.find_by_id(db, brand_id)
    if not brand:
        click.echo(f"Brand with ID {brand_id} not found.", err=True)
        return
    
    products = Product.find_by_brand(db, brand_id)
    if not products:
        click.echo(f"No products found for brand '{brand.name}'.")
        return
    
    click.echo(f"Products for brand '{brand.name}':")
    click.echo("ID\tName\tPrice\tSize\tColor\tQuantity")
    click.echo("--\t----\t-----\t----\t-----\t--------")
    for product in products:
        click.echo(f"{product.id}\t{product.name}\t{product.price}\t{product.size}\t{product.color or 'N/A'}\t{product.quantity}")
    db.close()

@cli.group()
def product():
    """Manage products"""
    pass

@product.command()
@click.option("--name", prompt="Product name", help="Name of the product")
@click.option("--price", prompt="Price", type=float, help="Price of the product")
@click.option("--size", prompt="Size", type=int, help="Size of the product")
@click.option("--brand-id", prompt="Brand ID", type=int, help="ID of the brand")
@click.option("--color", prompt="Color (optional)", default="", help="Color of the product")
@click.option("--quantity", prompt="Quantity", type=int, default=0, help="Quantity in stock")
def add(name, price, size, brand_id, color, quantity):
    """Add a new product"""
    db = get_session()
    try:
        product = Product.create(db, name, price, size, brand_id, color or None, quantity)
        click.echo(f"Product '{product.name}' added successfully with ID: {product.id}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)
    finally:
        db.close()

@product.command()
def list():
    """List all products"""
    db = get_session()
    products = Product.get_all(db)
    if not products:
        click.echo("No products found.")
        return
    
    click.echo("ID\tName\tBrand\tPrice\tSize\tColor\tQuantity")
    click.echo("--\t----\t-----\t-----\t----\t-----\t--------")
    for product in products:
        click.echo(f"{product.id}\t{product.name}\t{product.brand.name}\t{product.price}\t{product.size}\t{product.color or 'N/A'}\t{product.quantity}")
    db.close()

@product.command()
@click.argument("product_id", type=int)
def delete(product_id):
    """Delete a product by ID"""
    db = get_session()
    product = Product.find_by_id(db, product_id)
    if not product:
        click.echo(f"Product with ID {product_id} not found.", err=True)
        return
    
    try:
        product.delete(db)
        click.echo(f"Product '{product.name}' deleted successfully.")
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)
    finally:
        db.close()

@product.command()
@click.argument("name")
def search(name):
    """Search products by name"""
    db = get_session()
    products = Product.find_by_name(db, name)
    if not products:
        click.echo(f"No products found matching '{name}'.")
        return
    
    click.echo(f"Products matching '{name}':")
    click.echo("ID\tName\tBrand\tPrice\tSize\tColor\tQuantity")
    click.echo("--\t----\t-----\t-----\t----\t-----\t--------")
    for product in products:
        click.echo(f"{product.id}\t{product.name}\t{product.brand.name}\t{product.price}\t{product.size}\t{product.color or 'N/A'}\t{product.quantity}")
    db.close()

if __name__ == "__main__":
    cli()