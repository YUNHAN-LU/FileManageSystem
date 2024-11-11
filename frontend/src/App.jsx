import React, { useState, useEffect } from 'react';
import { Folder, File, ChevronRight, ChevronLeft } from 'lucide-react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const App = () => {
  const [currentItems, setCurrentItems] = useState([]);
  const [breadcrumbTrail, setBreadcrumbTrail] = useState([{ name: 'My Drive', data: [], id: 0 }]);
  const [contextMenuItem, setContextMenuItem] = useState(null);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    const fetchFileSystem = async () => {
      toast("Welcome to this demo site! Feel free to explore, all files and folders will be clear for no time");
      try {
        setLoading(true);
        const response = await fetch(`${import.meta.env.VITE_API_URL}/filesystem`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) throw new Error('Failed to fetch file system');

        const data = await response.json();
        console.log(data);
        setCurrentItems(data);
        setBreadcrumbTrail([{ name: 'My Drive', data, id: 0 }]);
        setLoading(false);
      } catch (error) {
        console.error(error.message);
      }
    };

    fetchFileSystem();
  }, []);



  const handleItemClick = (item) => {
    if (item.type === 'folder') {
      setCurrentItems(item.children);
      setBreadcrumbTrail([...breadcrumbTrail, { name: item.name, data: item.children, id: item.id }]);
    }
  };

  const handleBreadcrumbClick = (index) => {
    setCurrentItems(breadcrumbTrail[index].data);
    setBreadcrumbTrail(breadcrumbTrail.slice(0, index + 1));
  };

  const goBack = () => {
    if (breadcrumbTrail.length > 1) {
      const updatedBreadcrumbTrail = breadcrumbTrail.slice(0, -1);
      setCurrentItems(updatedBreadcrumbTrail[updatedBreadcrumbTrail.length - 1].data);
      setBreadcrumbTrail(updatedBreadcrumbTrail);
    }
  };

  const handleContextMenu = (event, item) => {
    event.preventDefault();
    setContextMenuItem({
      x: event.clientX,
      y: event.clientY,
      item,
    });
  };

  const closeContextMenu = () => {
    console.log(breadcrumbTrail)
    setContextMenuItem(null);
  };

  const handleOptionClick = async (option) => {
    if (!contextMenuItem) return;

    try {

      if (option === 'Delete') {
        setLoading(true);
        const response = await fetch(`${import.meta.env.VITE_API_URL}/filesystem/${contextMenuItem.item.id}`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) throw new Error('Delete failed');

        const updatedItems = currentItems.filter((item) => item.id !== contextMenuItem.item.id);
        setCurrentItems(updatedItems);
        breadcrumbTrail[breadcrumbTrail.length - 1].data = updatedItems;
        setBreadcrumbTrail(breadcrumbTrail);
        setLoading(false);
        toast.success("Success!");
      }


      if (option === 'Download') {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/filesystem/${contextMenuItem.item.id}/file`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) throw new Error('Download failed');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = contextMenuItem.item.name;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error(error.message);
    }

    setContextMenuItem(null);
  };

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('parentId', breadcrumbTrail[breadcrumbTrail.length - 1].id);
    formData.append('owner', 'visitor');

    try {
      setLoading(true);
      const response = await fetch(`${import.meta.env.VITE_API_URL}/filesystem/upload`, {
        method: 'POST',
        body: formData,
      });
      if (response.status === 409) {
        setLoading(false);
        toast.error("Duplicate File Name!");
        return;
      }
      else if (!response.ok) throw new Error('File upload failed');


      const result = await response.json();
      setCurrentItems([...currentItems, { name: file.name, type: 'file', id: result.id }]);

  
      setBreadcrumbTrail((prevBreadcrumbTrail) => {
        const updatedBreadcrumbTrail = [...prevBreadcrumbTrail];
        const lastItem = updatedBreadcrumbTrail[updatedBreadcrumbTrail.length - 1]; 
        lastItem.data = [...lastItem.data, { name: file.name, type: 'file', id: result.id, children: [] }]; 
        return updatedBreadcrumbTrail; 
      });
      setLoading(false);
      toast.success("Success!");
    } catch (error) {
      console.error(error.message);
    }

  };

  const handleCreateFolder = async (folderName) => {
    const formData = new FormData();
    formData.append('name', folderName);
    formData.append('parentId', breadcrumbTrail[breadcrumbTrail.length - 1].id);

    try {
      setLoading(true);
      const response = await fetch(`${import.meta.env.VITE_API_URL}/filesystem/folder`, {
        method: 'POST',
        body: formData,
      });

      if (response.status === 409) {
        setLoading(false);
        toast.error("Duplicate Folder Name!");
        return;
      }
      else if (!response.ok) throw new Error('File upload failed');

      const data = await response.json();
      setCurrentItems([...currentItems, { name: data.name, type: 'folder', id: data.id, children: [] }]);
      setBreadcrumbTrail((prevBreadcrumbTrail) => {
        const updatedBreadcrumbTrail = [...prevBreadcrumbTrail];
        const lastItem = updatedBreadcrumbTrail[updatedBreadcrumbTrail.length - 1]; 
        lastItem.data = [...lastItem.data, { name: data.name, type: 'folder', id: data.id, children: [] }]; 
        return updatedBreadcrumbTrail; 
      });
      setLoading(false);
      toast.success("Success!");
    } catch (error) {
      console.error(error.message);
    }

  };




  return (
    <div className="p-4 max-w-4xl mx-auto" onClick={closeContextMenu}>
      <div className="flex items-center mb-4">
        <h1 className="text-2xl font-bold mr-4">File Management System DEMO</h1>
        <input
          type="file"
          id="file-upload"
          style={{ display: 'none' }}
          onChange={(e) => {
            const file = e.target.files[0];
            if (file) handleFileUpload(file);
            e.target.value = '';
          }}
        />
        <label htmlFor="file-upload" className="cursor-pointer p-2 bg-blue-500 text-white rounded hover:bg-blue-600">Upload File</label>
        <button
          onClick={() => {
            const folderName = prompt("Enter folder name:");
            if (folderName) handleCreateFolder(folderName);
          }}
          className="ml-4 cursor-pointer p-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          New Folder
        </button>
      </div>

      <div className="flex items-center mb-4">
        <button
          onClick={goBack}
          disabled={breadcrumbTrail.length === 1}
          className="mr-2 p-1 rounded-full hover:bg-gray-200 disabled:opacity-50"
        >
          <ChevronLeft size={20} />
        </button>
        <div className="flex items-center">
          {breadcrumbTrail.map((crumb, index) => (
            <React.Fragment key={index}>
              {index > 0 && <ChevronRight size={16} className="mx-1 text-gray-400" />}
              <button
                onClick={() => handleBreadcrumbClick(index)}
                className="hover:underline focus:outline-none"
              >
                {crumb.name}
              </button>
            </React.Fragment>
          ))}
        </div>
      </div>

      {loading ?
        <div className="spinner border-b-2 border-gray-900 h-5 w-5 rounded-full animate-spin"></div>
        :

        <div style={{ height: window.innerHeight - 200 }} className="bg-white rounded-lg overflow-hidden">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-4">
            {currentItems.map((item) => (
              <div
                key={item.id}
                onContextMenu={(event) => handleContextMenu(event, item)}
                onClick={() => handleItemClick(item)}
                className="flex items-center p-2 rounded-lg hover:bg-gray-200  bg-[#f2f5f7] cursor-pointer"
              >
                {item.type === 'folder' ? (
                  <Folder className="mr-2 text-blue-500" size={24} />
                ) : (
                  <File className="mr-2 text-gray-500" size={24} />
                )}
                <span className="truncate">{item.name}</span>
              </div>
            ))}
          </div>
        </div>
      }

      {contextMenuItem && (
        <div className="absolute bg-white shadow-md rounded-lg p-2" style={{ top: contextMenuItem.y, left: contextMenuItem.x }}>
          <ul className="list-none">
            <li className="py-1 px-2 hover:bg-gray-200 cursor-pointer" onClick={() => handleOptionClick('Delete')}>Delete</li>
            <li className="py-1 px-2 hover:bg-gray-200 cursor-pointer" onClick={() => handleOptionClick('Download')}>Download</li>
          </ul>
        </div>
      )}

      <ToastContainer />
    </div>
  );
};

export default App;
