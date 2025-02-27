import { atom, useAtom } from "jotai";
import { useEffect, useRef, useState } from "react";

import { AvatarCreator } from "@readyplayerme/react-avatar-creator";
import { motion } from "framer-motion";
import { roomItemsAtom } from "./Room";
import { roomIDAtom, socket } from "./SocketManager";
import sdk from '@stackblitz/sdk';


export const buildModeAtom = atom(false);
export const shopModeAtom = atom(false);
export const draggedItemAtom = atom(null);
export const draggedItemRotationAtom = atom(0);

export const avatarUrlAtom = atom(
  localStorage.getItem("avatarURL") ||
  "https://models.readyplayer.me/64f0265b1db75f90dcfd9e2c.glb?meshlod=1&quality=medium"
);

const PasswordInput = ({ onClose, onSuccess }) => {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  // TODO: To make things properly we should have a loading state 😊

  const checkPassword = () => {
    socket.emit("passwordCheck", password);
  };

  useEffect(() => {
    socket.on("passwordCheckSuccess", () => {
      onSuccess();
      onClose();
    });
    socket.on("passwordCheckFail", () => {
      setError("Wrong password");
    });
    return () => {
      socket.off("passwordCheckSuccess");
      socket.off("passwordCheckFail");
    };
  });

  return (
    <div className="fixed z-10 grid place-items-center w-full h-full top-0 left-0">
      <div
        className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-50 backdrop-blur-sm"
        onClick={onClose}
      ></div>
      <div className="bg-white rounded-lg shadow-lg p-4 z-10">
        <p className="text-lg font-bold">Password</p>
        <input
          autoFocus
          type="text"
          className="border rounded-lg p-2"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <div className="space-y-2 mt-2">
          <button
            className="bg-green-500 text-white rounded-lg px-4 py-2 flex-1 w-full"
            onClick={checkPassword}
          >
            Enter
          </button>
          {error && <p className="text-red-500 text-sm">{error}</p>}
        </div>
      </div>
    </div>
  );
};

const ChatHistoryModal = ({ onClose, chatHistory }) => {
  return (
    <div className="fixed z-20 grid place-items-center w-full h-full top-0 left-0">
      <div
        className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-50 backdrop-blur-sm"
        onClick={onClose}
      ></div>
      <div className="bg-white rounded-lg shadow-lg p-4 z-20 max-w-md w-full">
        <p className="text-lg font-bold">Chat History</p>
        <div className="max-h-60 overflow-y-auto space-y-2 mt-2">
          {chatHistory.map((message, index) => (
            <div key={index} className={`flex flex-col ${message.senderId === "userId" ? "items-end" : "items-start"}`}>
              <span className="text-xs text-gray-500">{message.sender}</span>
              <div className={`bg-blue-500 text-white p-2 rounded-lg max-w-xs ${message.senderId === "userId" ? "ml-2" : "mr-2"}`}>
                <p className="text-sm">{message.text}</p>
              </div>
            </div>
          ))}
        </div>
        <button
          className="mt-4 bg-red-500 text-white rounded-lg px-4 py-2"
          onClick={onClose}
        >
          Close
        </button>
      </div>
    </div>
  );
};

function embedProject() {
  sdk.embedProjectId('stackBlitz-embed', 'css-custom-prop-color-values', {
    openFile: 'index.ts',
  });
}

const CodeInterfaceModal = ({ onClose }) => {
  useEffect(() => {
    embedProject();
  }, []);

  return (
    <div className="fixed z-20 grid place-items-center w-full h-full top-0 left-0">
      <div
        className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-50 backdrop-blur-sm"
        onClick={onClose}
      ></div>
      <div className="bg-white rounded-lg shadow-lg p-4 z-20 max-w-4xl w-full h-[80vh]">
        <div className="flex justify-between items-center mb-4">
          <p className="text-lg font-bold">Code Editor</p>
          <button
            className="text-gray-500 hover:text-gray-700"
            onClick={onClose}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
        <div className="h-[calc(100%-4rem)]">
          <div id="stackBlitz-embed" className="w-full h-full">
            <p>Loading editor...</p>
          </div>
        </div>
      </div>
    </div>
  );
};

function embedMarkdown(contents) {
  // Escape the contents to prevent issues with special characters
  const escapedContents = contents.replace(/\\/g, '\\\\') // Escape backslashes
    .replace(/`/g, '\\`'); // Escape backticks

  sdk.embedProject('stackBlitz-embed-marketing',
    {
      title: 'Marketing Requirements',
      description: 'Marketing requirements for the project',
      template: 'html',
      files: {
        'index.html': `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Embed Markdown in HTML</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>
  <div id="markdown-container">
    <!-- Markdown content will be rendered here -->
  </div>

  <script>
    const markdownContent = \`${escapedContents}\`;
    document.getElementById('markdown-container').innerHTML = marked.parse(markdownContent);
  </script>
</body>
</html>`
      }
    },
    {
      openFile: 'index.html',
      view: 'preview'
    }
  );
}


const MarketingInterfaceModal = ({ onClose, marketingRequirements }) => {
  useEffect(() => {
    embedMarkdown(marketingRequirements);
  }, []);

  return (
    <div className="fixed z-20 grid place-items-center w-full h-full top-0 left-0">
      <div
        className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-50 backdrop-blur-sm"
        onClick={onClose}
      ></div>
      <div className="bg-white rounded-lg shadow-lg p-4 z-20 max-w-4xl w-full h-[80vh]">
        <div className="flex justify-between items-center mb-4">
          <p className="text-lg font-bold">Code Editor</p>
          <button
            className="text-gray-500 hover:text-gray-700"
            onClick={onClose}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
        <div className="h-[calc(100%-4rem)]">
          <div id="stackBlitz-embed-marketing" className="w-full h-full">
            <p>Loading editor...</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export const UI = () => {
  const [buildMode, setBuildMode] = useAtom(buildModeAtom);
  const [shopMode, setShopMode] = useAtom(shopModeAtom);
  const [draggedItem, setDraggedItem] = useAtom(draggedItemAtom);
  const [draggedItemRotation, setDraggedItemRotation] = useAtom(
    draggedItemRotationAtom
  );
  const [_roomItems, setRoomItems] = useAtom(roomItemsAtom);
  const [passwordMode, setPasswordMode] = useState(false);
  const [avatarMode, setAvatarMode] = useState(false);
  const [avatarUrl, setAvatarUrl] = useAtom(avatarUrlAtom);
  const [roomID, setRoomID] = useAtom(roomIDAtom);
  const [passwordCorrectForRoom, setPasswordCorrectForRoom] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [showChatHistory, setShowChatHistory] = useState(false);
  const [showCodeInterfaceModal, setShowCodeInterfaceModal] = useState(false);
  const [showMarketingInterfaceModal, setShowMarketingInterfaceModal] = useState(false);
  const [marketingRequirements, setMarketingRequirements] = useState("");

  const leaveRoom = () => {
    socket.emit("leaveRoom");
    setRoomID(null);
    setBuildMode(false);
    setShopMode(false);
  };
  useEffect(() => {
    setPasswordCorrectForRoom(false); // PS: this is an ugly shortcut
  }, [roomID]);

  const ref = useRef();
  const [chatMessage, setChatMessage] = useState("");
  const sendChatMessage = () => {
    if (chatMessage.length > 0) {
      const newMessage = { senderId: "userId", sender: "You", text: chatMessage };
      socket.emit("chatMessage", chatMessage);
      setChatHistory((prev) => [...prev, newMessage]);
      setChatMessage("");
    }
  };

  useEffect(() => {
    socket.on("marketingRequirementsUpdate", (content) => {
      setMarketingRequirements(content);
    });

    return () => {
      socket.off("marketingRequirementsUpdate");
    };
  }, []);

  // Movement Data Update
  useEffect(() => {
    const handleMovementDataUpdate = (data) => {
      console.log("Received movement data:", data);

      if (roomID === 1 && data?.Movement) {  // Only handle movement in CEO's room
        // Convert grid coordinates to match game's coordinate system
        const targetX = data.Movement.x; // Multiply by gridDivision (2)
        const targetY = data.Movement.y;

        // Emit move event specifically for CEO
        socket.emit("move",
          [8, 11],  // CEO's starting position from default.json
          [targetX, targetY]   // Target position from movement.json
        );

        // Handle any CEO messages if needed
        if (data.Marketing?.Speech) {
          socket.emit("ceoChatMessage", data.Marketing.Speech);
        }
      }
    };

    socket.on("movementDataUpdate", handleMovementDataUpdate);

    return () => {
      socket.off("movementDataUpdate", handleMovementDataUpdate);
    };
  }, [roomID]);

  // Player Chat Message
  useEffect(() => {
    const handlePlayerChatMessage = (data) => {
      if (data.id !== socket.id) {
        const sender = data.id === "ceo" ? "CEO" : `User ${data.id.slice(0, 4)}`;
        const newMessage = {
          senderId: data.id,
          sender: sender,
          text: data.message,
        };
        setChatHistory((prev) => [...prev, newMessage]);
      }
    };

    socket.on("playerChatMessage", handlePlayerChatMessage);

    return () => {
      socket.off("playerChatMessage", handlePlayerChatMessage);
    };
  }, []); // Empty dependency array since it doesn't rely on external state


  return (
    <>
      <motion.div
        ref={ref}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 0.5 }}
      >
        {avatarMode && (
          <AvatarCreator
            subdomain="wawa-sensei-tutorial"
            className="fixed top-0 left-0 z-[999999999] w-full h-full" // have to put a crazy z-index to be on top of HTML generated by Drei
            onAvatarExported={(event) => {
              let newAvatarUrl =
                event.data.url === avatarUrl.split("?")[0]
                  ? event.data.url.split("?")[0] + "?" + new Date().getTime()
                  : event.data.url;
              newAvatarUrl +=
                (newAvatarUrl.includes("?") ? "&" : "?") +
                "meshlod=1&quality=medium";
              setAvatarUrl(newAvatarUrl);
              localStorage.setItem("avatarURL", newAvatarUrl);
              if (roomID) {
                socket.emit("characterAvatarUpdate", newAvatarUrl);
              }
              setAvatarMode(false);
            }}
          />
        )}
        {passwordMode && (
          <PasswordInput
            onClose={() => setPasswordMode(false)}
            onSuccess={() => {
              setBuildMode(true);
              setPasswordCorrectForRoom(true);
            }}
          />
        )}
        <div className="fixed inset-4 flex items-center justify-end flex-col pointer-events-none select-none">
          {roomID && !shopMode && !buildMode && (
            <div className="pointer-events-auto p-4 flex items-center space-x-4">
              <input
                type="text"
                className="w-56 border px-5 p-4 h-full rounded-full"
                placeholder="Message the CEO..."
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    sendChatMessage();
                  }
                }}
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
              />
              <button
                className="p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={sendChatMessage}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
                  />
                </svg>
              </button>
            </div>
          )}
          <div className="flex items-center space-x-4 pointer-events-auto">
            {roomID && !shopMode && !buildMode && (
              <button
                className="p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={leaveRoom}
              >
                LOBBY
              </button>
            )}
            {/* BACK */}
            {(buildMode || shopMode) && draggedItem === null && (
              <button
                className="p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={() => {
                  shopMode ? setShopMode(false) : setBuildMode(false);
                }}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3"
                  />
                </svg>
              </button>
            )}
            {/* AVATAR */}
            {!buildMode && !shopMode && (
              <button
                className="p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={() => setAvatarMode(true)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
                  />
                </svg>
              </button>
            )}
            {/* DANCE */}
            {roomID && !buildMode && !shopMode && (
              <button
                className="p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={() => socket.emit("dance")}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9 9l10.5-3m0 6.553v3.75a2.25 2.25 0 01-1.632 2.163l-1.32.377a1.803 1.803 0 11-.99-3.467l2.31-.66a2.25 2.25 0 001.632-2.163zm0 0V2.25L9 5.25v10.303m0 0v3.75a2.25 2.25 0 01-1.632 2.163l-1.32.377a1.803 1.803 0 01-.99-3.467l2.31-.66A2.25 2.25 0 009 15.553z"
                  />
                </svg>
              </button>
            )}
            {/* BUILD */}
            {roomID && !buildMode && !shopMode && (
              <button
                className="p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={() => {
                  if (!passwordCorrectForRoom) {
                    setPasswordMode(true);
                  } else {
                    setBuildMode(true);
                  }
                }}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
                  />
                </svg>
              </button>
            )}
            {/* SHOP */}
            {buildMode && !shopMode && draggedItem === null && (
              <button
                className="p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={() => setShopMode(true)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M13.5 21v-7.5a.75.75 0 01.75-.75h3a.75.75 0 01.75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349m-16.5 11.65V9.35m0 0a3.001 3.001 0 003.75-.615A2.993 2.993 0 009.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 002.25 1.016c.896 0 1.7-.393 2.25-1.016a3.001 3.001 0 003.75.614m-16.5 0a3.004 3.004 0 01-.621-4.72L4.318 3.44A1.5 1.5 0 015.378 3h13.243a1.5 1.5 0 011.06.44l1.19 1.189a3 3 0 01-.621 4.72m-13.5 8.65h3.75a.75.75 0 00.75-.75V13.5a.75.75 0 00-.75-.75H6.75a.75.75 0 00-.75.75v3.75c0 .415.336.75.75.75z"
                  />
                </svg>
              </button>
            )}

            {/* ROTATE */}
            {buildMode && !shopMode && draggedItem !== null && (
              <button
                className="p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={() =>
                  setDraggedItemRotation(
                    draggedItemRotation === 3 ? 0 : draggedItemRotation + 1
                  )
                }
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99"
                  />
                </svg>
              </button>
            )}
            {/* CANCEL */}
            {buildMode && !shopMode && draggedItem !== null && (
              <button
                className="p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={() => setDraggedItem(null)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            )}
            {/* REMOVE ITEM */}
            {buildMode && !shopMode && draggedItem !== null && (
              <button
                className="p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={() => {
                  setRoomItems((prev) => {
                    const newItems = [...prev];
                    newItems.splice(draggedItem, 1);
                    return newItems;
                  });
                  setDraggedItem(null);
                }}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
                  />
                </svg>
              </button>
            )}
          </div>
        </div>
        {/* Chat History Button - Only shown when in a room */}
        {roomID && (
          <>
            <button
              className="fixed top-4 right-4 p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
              onClick={() => setShowChatHistory(true)}
            >
              {/* Chat History Icon */}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 512 512"
                className="w-6 h-6"
              >
                <path
                  d="M96 368Q83 368 74 359 64 349 64 336L64 128Q64 114 74 105 83 96 96 96L416 96Q430 96 439 105 448 114 448 128L448 336Q448 349 439 359 430 368 416 368L256 368 160 464 160 368 96 368Z"
                  fill="none"
                  stroke="white"
                  strokeWidth="30"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </button>

            {/* Marketing Requirements Button */}
            {roomID == 2 && (
              <button
                className="fixed top-20 right-4 p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={() => setShowMarketingInterfaceModal(true)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 4.5v15m7.5-7.5h-15"
                  />
                </svg>
              </button>
            )}

            {/* StackBlitz Button */}
            {roomID == 3 && (
              <button
                className="fixed top-20 right-4 p-4 rounded-full bg-slate-500 text-white drop-shadow-md cursor-pointer hover:bg-slate-800 transition-colors"
                onClick={() => setShowCodeInterfaceModal(true)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 4.5v15m7.5-7.5h-15"
                  />
                </svg>
              </button>
            )}
          </>
        )}

        {/* Chat History Modal */}
        {showChatHistory && (
          <ChatHistoryModal
            onClose={() => setShowChatHistory(false)}
            chatHistory={chatHistory}
          />
        )}

        {showMarketingInterfaceModal && (
          <MarketingInterfaceModal
            onClose={() => setShowMarketingInterfaceModal(false)}
            marketingRequirements={marketingRequirements}
          />
        )}

        {/* Add the code modal */}
        {showCodeInterfaceModal && <CodeInterfaceModal onClose={() => setShowCodeInterfaceModal(false)} />}
      </motion.div>
    </>
  );
};
