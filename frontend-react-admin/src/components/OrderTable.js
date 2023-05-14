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
        {orders.map((orders) => (
          <tr key={orders.order_id}>
            <td  className="table-row">>{orders.order_id}</td>
            <td  className="table-row">>{orders.order_date}</td>
            <td  className="table-row">>{orders.order_discount}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default OrderTable;