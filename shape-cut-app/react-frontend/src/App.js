import React, { useState, useRef } from 'react';
import { Button, Container, Typography, Box, Card, CardContent, CircularProgress } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import './App.css';

const theme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  const [image, setImage] = useState(null);
  const [recommendations, setRecommendations] = useState('');
  const [loading, setLoading] = useState(false);
  const videoRef = useRef(null);
  const fileInputRef = useRef(null);

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
  };

  const captureImage = async () => {
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas.getContext('2d').drawImage(videoRef.current, 0, 0);
    const imageUrl = canvas.toDataURL('image/png');
    setImage(imageUrl);
    sendImageToServer(imageUrl);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setImage(e.target.result);
        sendImageToServer(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const sendImageToServer = async (imageUrl) => {
    const blob = await (await fetch(imageUrl)).blob();
    const formData = new FormData();
    formData.append('image', blob, 'capture.png');

    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setRecommendations(data.recommendations);
    } catch (error) {
      console.error('Error uploading image:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md">
        <Box sx={{ my: 4, textAlign: 'center' }}>
          <Typography variant="h2" component="h1" gutterBottom>
            Shape Cut
          </Typography>
          <Box className="camera-container" sx={{ border: '1px solid grey', p: 2, my: 2 }}>
            <video ref={videoRef} autoPlay playsInline style={{ width: '100%', maxWidth: '500px' }}></video>
          </Box>
          <Button variant="contained" onClick={startCamera} sx={{ mr: 1 }}>Start Camera</Button>
          <Button variant="contained" onClick={captureImage} sx={{ mr: 1 }}>Capture & Analyze</Button>
          <Button variant="contained" onClick={() => fileInputRef.current.click()}>Upload Image</Button>
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileChange}
            accept="image/*"
          />

          {image && (
            <Box className="image-preview" sx={{ my: 2 }}>
              <Typography variant="h5">Your Image:</Typography>
              <img src={image} alt="Captured" style={{ maxWidth: '100%', maxHeight: '300px' }} />
            </Box>
          )}

          {loading && <CircularProgress sx={{ my: 2 }} />}

          {recommendations && (
            <Card sx={{ my: 2 }}>
              <CardContent>
                <Typography variant="h5">Hairstyle Recommendations:</Typography>
                <Typography variant="body1">{recommendations}</Typography>
              </CardContent>
            </Card>
          )}
        </Box>
        <footer style={{ textAlign: 'center', padding: '20px' }}>
          <Typography variant="body2">
            developed by mujahid ..bs bioinfromatics hazara uinversity mansehra ...03495474869
          </Typography>
        </footer>
      </Container>
    </ThemeProvider>
  );
}

export default App;