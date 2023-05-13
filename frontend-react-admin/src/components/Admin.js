import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CustomerTable from './CustomerTable';
import OrderTable from './OrderTable';
import ItemTable from './ItemTable';

const Admin = () => {
  const [customers, setCustomers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchCustomers();
    fetchOrders();
    fetchItems();
  }, []);

  const fetchCustomers = async () => {
    const response = await axios.get('http://localhost:5000/customers');
    setCustomers(response.data);
  };

  const fetchOrders = async () => {
    const response = await axios.get('http://localhost:5000/orders');
    setOrders(response.data);
  };

  const fetchItems = async () => {
    const response = await axios.get('http://localhost:5000/items');
    setItems(response.data);
  };

  return (
    <div>
      <h2>Admin Page</h2>
      <h3>Customers</h3>
      <CustomerTable customers={customers} />
      <h3>Orders</h3>
      <OrderTable orders={orders} />
      <h3>Items</h3>
      <ItemTable items={items} />
    </div>
  );
};

export default Admin;
