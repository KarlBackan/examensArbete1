import React from 'react';

const CustomerTable = ({ customers }) => {
  return (
    <table>
      <thead className="table-header">
        <tr>
          <th>ID</th>
          <th>Customer Since</th>
          <th>Amount of Orders</th>
        </tr>
      </thead>
      <tbody>
        {customers.map((customer) => (
          <tr key={customer.id}>
            <td  className="table-row">>{customer.customer_id}< /td>
            <td  className="table-row">>{customer.customer_since}</td>
            <td  className="table-row">>{customer.amount_of_orders}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default CustomerTable;
