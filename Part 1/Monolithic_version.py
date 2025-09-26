import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit
)
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# === DATABASE SETUP ===
# Adjust port to 5433 if you're using Docker with custom port
DATABASE_URL = "postgresql+psycopg2://inventory:inventory@localhost:5433/inventory"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# === PRODUCT TABLE ===
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# === GUI CLASS ===
class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DataMart Inventory (Monolith)")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Input fields
        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.price_input = QLineEdit()

        layout.addWidget(QLabel("Product ID:"))
        layout.addWidget(self.id_input)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Quantity:"))
        layout.addWidget(self.quantity_input)
        layout.addWidget(QLabel("Price:"))
        layout.addWidget(self.price_input)

        # Buttons
        btn_layout = QHBoxLayout()
        create_btn = QPushButton("Create")
        read_btn = QPushButton("View All")
        update_btn = QPushButton("Update")
        delete_btn = QPushButton("Delete")

        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(read_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)

        # Output area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        # Set layout
        self.setLayout(layout)

        # Button events
        create_btn.clicked.connect(self.create_product)
        read_btn.clicked.connect(self.view_products)
        update_btn.clicked.connect(self.update_product)
        delete_btn.clicked.connect(self.delete_product)

    # === CRUD FUNCTIONS ===
    def create_product(self):
        try:
            id = int(self.id_input.text())
            name = self.name_input.text().strip()
            quantity = int(self.quantity_input.text())
            price = float(self.price_input.text())

            if quantity < 0 or price < 0:
                self.output.setText("❌ Quantity and price must be ≥ 0.")
                return

            session = SessionLocal()
            product = Product(id=id, name=name, quantity=quantity, price=price)
            session.add(product)
            session.commit()
            session.close()
            self.output.setText("✅ Product created.")

        except Exception as e:
            self.output.setText(f"❌ Error: {e}")

    def view_products(self):
        session = SessionLocal()
        products = session.query(Product).all()
        session.close()

        if not products:
            self.output.setText("ℹ️ No products found.")
        else:
            text = "\n".join(
                f"{p.id} | {p.name} | Qty: {p.quantity} | ${p.price:.2f}" for p in products
            )
            self.output.setText(text)

    def update_product(self):
        try:
            id = int(self.id_input.text())
            name = self.name_input.text().strip()
            quantity = int(self.quantity_input.text())
            price = float(self.price_input.text())

            if quantity < 0 or price < 0:
                self.output.setText("❌ Quantity and price must be ≥ 0.")
                return

            session = SessionLocal()
            product = session.query(Product).filter_by(id=id).first()

            if product:
                product.name = name
                product.quantity = quantity
                product.price = price
                session.commit()
                self.output.setText("✅ Product updated.")
            else:
                self.output.setText("❌ Product not found.")

            session.close()
        except Exception as e:
            self.output.setText(f"❌ Error: {e}")

    def delete_product(self):
        try:
            id = int(self.id_input.text())

            session = SessionLocal()
            product = session.query(Product).filter_by(id=id).first()

            if product:
                session.delete(product)
                session.commit()
                self.output.setText("✅ Product deleted.")
            else:
                self.output.setText("❌ Product not found.")

            session.close()
        except Exception as e:
            self.output.setText(f"❌ Error: {e}")

# === RUN APP ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())
