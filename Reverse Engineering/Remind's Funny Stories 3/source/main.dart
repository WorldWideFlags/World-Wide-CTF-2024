import 'package:flutter/material.dart';
import 'dart:io';
import 'package:video_player/video_player.dart';
import 'package:flutter/services.dart';
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:stringcare/stringcare.dart';
import 'package:jailbreak_root_detection/jailbreak_root_detection.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Remind\'s funny stories 3',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.pink),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Remind\'s funny stories 3'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;
  late VideoPlayerController _videoController;
  late Future<void> _initializeVideoPlayerFuture;
  var _encryptedMessage =
      "CXHoq5mV1jMA+63Sa7+IwhmhZWUXDL69B+wSB01uEQc63QWB0ZIeOiZtheLJpD0s2sC3s2+9FiWyRA+c1Y+vYw=="
          .obfuscate(); // Replace with your encrypted message
  var _aesKey = "0h_g0d_sup3r_k3y_is_here_gsirjcu"
      .obfuscate(); // Replace with your AES key
  var _aesIV = "16_bytes_key_len".obfuscate(); // Replace with your AES IV

  @override
  void initState() {
    super.initState();
    _initializeVideoPlayer();
  }

  void _initializeVideoPlayer() {
    _videoController = VideoPlayerController.network(
      'https://github.com/Qynklee/Qynklee/raw/main/assets/media/remind3.mp4',
    );
    _initializeVideoPlayerFuture = _videoController.initialize();
    _videoController.setLooping(true);
    _processCheckJailbreakRoot().then((isSecure) {
      if (!isSecure) {
        setState(() {});
      }
    });
  }

  @override
  void dispose() {
    _videoController.dispose();
    super.dispose();
  }

  void _incrementCounter() {
    setState(() {
      _counter++;
      if (_counter >= 10000000) {
        _showWinnerDialog();
      }
    });
  }

  void _showWinnerDialog() {
    final decryptedMessage = _decryptMessage(_encryptedMessage);
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Congrat! Remind got your heart! <3'),
          content: Text(decryptedMessage),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Clipboard.setData(ClipboardData(text: decryptedMessage));
                Navigator.of(context).pop();
              },
              child: const Text('Copy'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Close'),
            ),
          ],
        );
      },
    );
  }

  String _decryptMessage(String encryptedMessage) {
    final key = encrypt.Key.fromUtf8(_aesKey.reveal());
    final iv = encrypt.IV.fromUtf8(_aesIV.reveal());
    final encrypter = encrypt.Encrypter(
        encrypt.AES(key, padding: 'PKCS7', mode: encrypt.AESMode.cbc));
    final encrypted = encrypt.Encrypted.fromBase64(encryptedMessage.reveal());
    final decrypted = encrypter.decrypt(encrypted, iv: iv);
    return decrypted;
  }

  Future<bool> _processCheckJailbreakRoot() async {
    if (Platform.isAndroid) {
      try {
        final isJailBroken = await JailbreakRootDetection.instance.isJailBroken;
        // final checkForIssues =
        //     await JailbreakRootDetection.instance.checkForIssues;
        final isDevMode = await JailbreakRootDetection.instance.isDevMode;
        final isRealDevice = await JailbreakRootDetection.instance.isRealDevice;

        if (isDevMode) {
          _showSecurityDialog('Device developer mode is on.');
          return false;
        }

        if (isRealDevice) {
        } else {
          _showSecurityDialog('Device emulator detected.');
          return false;
        }

        // if (checkForIssues.isNotEmpty) {
        //   _showSecurityDialog('Device has security issues.');
        //   return false;
        // }

        if (isJailBroken) {
          _showSecurityDialog('Device is rooted or jailbroken.');
          return false;
        }
      } catch (e) {
        print(e);
      }
    }
    return true;
  }

  void _showSecurityDialog(String message) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Security Alert'),
          content: Text(message),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                //Navigator.of(context).pop();
                //SystemNavigator.pop();
                exit(0);
              },
              child: const Text('Close'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'Heart 10 million times to receive the flag!',
            ),
            const Text("Number of times heart dropped: "),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 20),
            FutureBuilder(
              future: _initializeVideoPlayerFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.done) {
                  return AspectRatio(
                    aspectRatio: _videoController.value.aspectRatio,
                    child: VideoPlayer(_videoController),
                  );
                } else {
                  return const CircularProgressIndicator();
                }
              },
            ),
            const SizedBox(height: 20),
            FloatingActionButton(
              onPressed: () {
                setState(() {
                  if (_videoController.value.isPlaying) {
                    _videoController.pause();
                  } else {
                    _videoController.play();
                  }
                });
              },
              tooltip: 'Play/Pause Video',
              child: Icon(
                _videoController.value.isPlaying
                    ? Icons.pause
                    : Icons.play_arrow,
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Drop your heart',
        child: const Icon(Icons.favorite),
      ),
    );
  }
}
