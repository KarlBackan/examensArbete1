import React from 'react';

const CustomerTable = ({ customers }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Customer Since</th>
          <th>Amount of Orders</th>
        </tr>
      </thead>
      <tbody>
        {customers.map((customer) => (
          <tr key={customer.id}>
            <td>{customer.id}</td>
            <td>{customer.customer_since}</td>
            <td>{customer.amount_of_orders}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default CustomerTable;
