import React from 'react';

const ItemTable = ({ items }) => {
  return (
    <table>
      <thead className="table-header">
        <tr>
          <th>Item ID</th>
          <th>Name</th>
          <th>Price</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.item_id}>
            <td  className="table-row">>{item.item_id}</td>
            <td  className="table-row">>{item.item_name}</td>
            <td  className="table-row">>{item.item_price}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ItemTable;