import {React, useState, useEffect} from 'react'
import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem from '@mui/lab/TreeItem';
import axios from 'axios';

const Navigator = (props) => {
  const [data, setData] = useState({})

  useEffect(() => {
    axios.post(`/prod/endpoint1`, { name: 'hello from react' })
    .then((res) => {
      console.log(res.data);
      setData(res.data)
    });      
  }, [])

  const renderTree = (nodes) => (
    <TreeItem key={nodes.id} nodeId={nodes.id} label={nodes.name}>
      {Array.isArray(nodes.children)
        ? nodes.children.map((node) => renderTree(node))
        : null}
    </TreeItem>
  );

  return (
      <TreeView
        aria-label="rich object"
        defaultCollapseIcon={<ExpandMoreIcon />}
        defaultExpanded={['root']}
        defaultExpandIcon={<ChevronRightIcon />}
        sx={{ height: '100vh', flexGrow: 1, maxWidth: 400, overflowY: 'auto' }}
      >
        {renderTree(data)}
      </TreeView>
  );
}

export default Navigator;