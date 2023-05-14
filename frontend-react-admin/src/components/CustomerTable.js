import React from 'react';

const CustomerTable = ({ customers }) => {
  return (
    <table>
      <thead className="table-header">
        <tr>
          <th>ID</th>
            <th>Customer Name</th>
          <th>Customer Since</th>
          <th>Amount of Orders</th>
            <th>Customer Address</th>
        </tr>
      </thead>
      <tbody>
        {customers.map((customers) => (
          <tr key={customers.id}>
            <td  className="table-row">>{customers.customer_id}< /td>
              <td  className="table-row">>{customers.customer_name}< /td>
            <td  className="table-row">>{customers.customer_since}</td>
            <td  className="table-row">>{customers.amount_of_orders}</td>
              <td  className="table-row">>{customers.customer_address}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default CustomerTable;
