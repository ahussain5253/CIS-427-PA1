
-- @block

CREATE TABLE customer (
    id Integer AUTO_INCREMENT not null primary key,
    first_name VARCHAR(50) not null,
    last_name VARCHAR(50) not null,
    email VARCHAR(50) not null,
    phone VARCHAR(50) not null,
    CONSTRAINT chk_email CHECK (email LIKE '%@%')
);

CREATE TABLE customer_address (
    id Integer AUTO_INCREMENT not null primary key,
    customer_id Integer not null,
    address VARCHAR(255) not null,
    city VARCHAR(50) not null,
    state VARCHAR(50) not null,
    zip VARCHAR(50) not null,
    CONSTRAINT fk_customer_billing_customer_id FOREIGN KEY (customer_id) REFERENCES customer(id)
);

CREATE TABLE customer_billing (
    id Integer AUTO_INCREMENT not null primary key,
    customer_id Integer not null,
    address_id Integer not null,
    card_number VARCHAR(16) not null,
    card_type VARCHAR(50) not null,
    card_cvv VARCHAR(4) not null,
    card_expiration_date DATE not null,
    CONSTRAINT fk_customer_billing_info_customer_id FOREIGN KEY (customer_id) REFERENCES customer(id),
    CONSTRAINT fk_customer_billing_info_address_id FOREIGN KEY (address_id) REFERENCES customer_address(id)
);

CREATE TABLE product (
    id int AUTO_INCREMENT not null primary key,
    name VARCHAR(50) not null,
    price DECIMAL(10,2) not null,
    description VARCHAR(255) not null,
    CONSTRAINT chk_price CHECK (price > 0)
);

CREATE TABLE product_image (
    product_id Integer not null,
    image_url VARCHAR(255) not null,
    CONSTRAINT fk_product_image_product_id FOREIGN KEY (product_id) REFERENCES product(id)
);


CREATE TABLE product_review (
    product_id Integer not null,
    customer_id Integer not null,
    review VARCHAR(255) not null,
    rating Integer not null,
    CONSTRAINT product_review_rating CHECK (rating >= 1 AND rating <= 5),
    CONSTRAINT fk_product_review_product_id FOREIGN KEY (product_id) REFERENCES product(id),
    CONSTRAINT fk_product_review_customer_id FOREIGN KEY (customer_id) REFERENCES customer(id)
);

CREATE TABLE `order` (
    id int AUTO_INCREMENT not null primary key,
    customer_id int not null,
    order_date DATE not null,
    shipping_address_id int not null,
    CONSTRAINT fk_order_customer_id FOREIGN KEY (customer_id) REFERENCES customer(id),
    CONSTRAINT fk_order_shipping_address_id FOREIGN KEY (shipping_address_id) REFERENCES customer_address(id)
);

CREATE TABLE order_item (
    order_id Integer not null,
    product_id Integer not null,
    quantity Integer not null,
    CONSTRAINT fk_order_item_order_id FOREIGN KEY (order_id) REFERENCES `order`(id),
    CONSTRAINT fk_order_item_product_id FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE `transaction` (
    id Integer AUTO_INCREMENT not null primary key,
    order_id Integer not null,
    transaction_date DATE not null,
    transaction_amount DECIMAL(10,2) not null,
    billing_id Integer not null,
    CONSTRAINT fk_transaction_order_id FOREIGN KEY (order_id) REFERENCES `order`(id),
    CONSTRAINT fk_transaction_billing_id FOREIGN KEY (billing_id) REFERENCES customer_billing(id)
);

CREATE TABLE shipping_service (
    name VARCHAR(50) not null primary key,
    phone VARCHAR(50) not null,
    email VARCHAR(50) not null,
    website VARCHAR(128) not null,
    CONSTRAINT chk_email CHECK (email LIKE '%@%')
);

CREATE TABLE shipment (
    id Integer AUTO_INCREMENT not null primary key,
    order_id Integer not null,
    shipping_service_name VARCHAR(50) not null,
    tracking_number VARCHAR(50) not null,
    assigned_date DATE not null,
    assigned_by Integer not null,
    CONSTRAINT fk_shipment_order_id FOREIGN KEY (order_id) REFERENCES `order`(id),
    CONSTRAINT fk_shipment_shipping_service_name FOREIGN KEY (shipping_service_name) REFERENCES shipping_service(name),
    CONSTRAINT fk_shipment_assigned_by FOREIGN KEY (assigned_by) REFERENCES worker(emp_id)
);


ER_PARSE_ERROR: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'CREATE TABLE customer_address (
 