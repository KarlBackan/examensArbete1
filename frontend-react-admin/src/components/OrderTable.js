import React, { useState, useEffect } from 'react';
import axios from 'axios';

const OrderTable = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    const response = await axios.get('/api/orders');
    setOrders(response.data);
  };

  return (
    <table>
      <thead>
        <tr>
          <th>Order ID</th>
          <th>Customer ID</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        {orders.map((order) => (
          <tr key={order.order_id}>
            <td>{order.order_id}</td>
            <td>{order.customer_id}</td>
            <td>{order.date}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default OrderTable;
