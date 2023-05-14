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
        {items.map((items) => (
          <tr key={items.item_id}>
            <td  className="table-row">>{items.item_id}</td>
            <td  className="table-row">>{items.item_name}</td>
            <td  className="table-row">>{items.item_price}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ItemTable;