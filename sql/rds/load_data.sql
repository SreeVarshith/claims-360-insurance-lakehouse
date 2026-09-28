-- Load the generated CSV files (run inside psql, from the folder that
-- contains the files uploaded to CloudShell).
-- \copy is a psql client command, so the file is read from the client side.
-- Load customers first: policies has a foreign key to customers.

-- Copy data of customers.csv to customers table
\copy customers(cust_id, name, email, risk_segment) FROM 'customers.csv' DELIMITER ',' CSV HEADER;

-- Copy data of policies.csv to policies table
\copy policies(policy_id, cust_id, policy_type, premium_amount) FROM 'policies.csv' DELIMITER ',' CSV HEADER;
