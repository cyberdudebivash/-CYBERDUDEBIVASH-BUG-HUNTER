import React from "react";

function AssetTable({ assets }) {

  return (
    <table border="1">
      <thead>
        <tr>
          <th>Asset</th>
        </tr>
      </thead>

      <tbody>

        {assets.map((a, index) => (
          <tr key={index}>
            <td>{a}</td>
          </tr>
        ))}

      </tbody>
    </table>
  );
}

export default AssetTable;