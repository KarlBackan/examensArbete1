import React from 'react';

const OrderTable = ({ orders }) => {
  return (
    <table>
      <thead className="table-header">
        <tr>
          <th>Order ID</th>
          <th>Order Date</th>
          <th>Order Discount</th>
        </tr>
      </thead>
      <tbody>
        {orders.map((order) => (
          <tr key={order.order_id}>
            <td  className="table-row">>{order.order_id}</td>
            <td  className="table-row">>{order.order_date}</td>
            <td  className="table-row">>{order.order_discount}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default OrderTable;