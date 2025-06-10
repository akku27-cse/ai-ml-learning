import React, { useState } from 'react';
import {
  SafeAreaView,
  TextInput,
  Button,
  FlatList,
  Text,
  View,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';

const GEMINI_API_KEY = 'AIzaSyDKo2knzBu8uBnB3-mnMYwJJ2Mvhx6FlgQ'; 
const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`;
const CUSTOM_RESPONSES: Record<string, string> = {
  "contact": "You can contact us at apexiumtechnologies@gmail.com or call +91 8918080399. We're available 24/7.",

  "about": "PupHub is a comprehensive social media and service platform designed for pet owners. You can share your pet's life moments, book services like grooming and creche, read pet-related news, chat with other pet lovers, and find nearby veterinarians, clinics, groomers, and pharmacies. PupHub helps you manage every aspect of your pet’s care while connecting with a like-minded community.",

  "features": "PupHub offers: 🐾 Pet Profile Management, 📍 Vet & Clinic Locator, 🧼 Grooming & Creche Booking, 📰 Pet News Feed, 📖 Blog & Story Sharing, 💬 In-app Chat, 📸 Media Sharing, 🧾 Pet Health Tracking, 🆘 Emergency Contact Directory, and 🛒 Partner Dashboard for service providers.",

  "refund": "We offer a 30-day money-back guarantee for subscription-based services. For refunds, please contact support@puphub.app with your payment details and registered mobile number.",

  "privacy": "Your privacy is important to us. PupHub never shares your personal or pet data with third parties without your consent. To know more, read our privacy policy at puphub.app/privacy.",

  "pricing": "PupHub is completely free for pet parents. Service providers can join the PupHub Partner program for premium features at a subscription fee. Contact us for the latest pricing details.",

  "services": "We offer the following services: 🧼 Pet Grooming, 🏠 Creche/Daycare, 👨‍⚕️ Vet Appointments, 🏥 Clinic Visits, 🆘 Emergency Helplines, 🐶 Pet Adoption Listings, 🧾 Service Booking History, and 📍 PIN-based Service Search.",

  "partner": "If you're a vet, groomer, clinic, creche, or pharmacy, join our PupHub Partner Program to grow your reach. Register at puphub.app/partner or email partners@puphub.app.",

  "support": "Need help? Visit the Help Desk in the app or email support@puphub.app. We typically respond within 24 hours.",

  "location": "PupHub currently serves pet lovers in Bengaluru, Kolkata, Mumbai, and Delhi. More cities are being added soon!",

  "upload_story": "To upload a story or blog:\n1. Open the PupHub app.\n2. Go to the 'Stories' or 'Blog' section.\n3. Tap the '+' button.\n4. Add a title, description, and upload images or videos.\n5. Tap 'Post' to publish your story.\nYour story will now be visible to the PupHub community!",

  "find_service": "To find pet services near you:\n1. Open the PupHub app.\n2. Tap on 'Find Services' or use the search bar.\n3. Choose a service type: Grooming, Creche, Vet, Clinic, or Pharmacy.\n4. Enable location access or enter your area PIN code.\n5. Browse through the listed service providers with reviews and contact options.",

  "chat": "To chat with other pet lovers:\n1. Open the PupHub app.\n2. Tap the 'Chat' icon.\n3. Search by username or browse active users.\n4. Tap a user to start chatting.\nYou can send text, emojis, and share pet images easily!",

  "blog_guidelines": "When writing a blog:\n- Keep content pet-related.\n- Be respectful and use appropriate language.\n- Include images or videos for better engagement.\n- Avoid third-party promotions unless approved by PupHub.",

  "media_chat": "Yes, PupHub chat allows image and media sharing! Send pictures of your pets, share vet prescriptions, and make conversations more lively.",

  "pet_health_tracking": "PupHub includes tools to track vaccinations, vet visits, medication schedules, and health notes for your pets.",

  "lost_and_found": "PupHub’s Lost & Found section lets users report missing pets and browse found animals posted by others. Help reunite pets with their families!",

  "reminders": "Set reminders easily in PupHub:\n- Tap 'Reminders' in your pet’s profile.\n- Add events like vet visits, grooming, feeding time.\n- Get notifications right on time!",

  "events": "Join and host pet events in your city! Find or post meetups, training workshops, and adoption drives in the 'Events' section of PupHub.",

  "adoption": "Looking to adopt a furry friend? Visit the 'Adoption' tab to browse pets listed by verified shelters and rescue partners.",

  "reviews": "PupHub lets you rate and review services you've used. Your feedback helps other pet parents make informed choices.",

  "platforms": "PupHub is available on both Android (Play Store) and iOS (App Store). Download now to get started!",

  "pet_profile": "Create a pet profile by going to 'My Pets' section. Add photo, name, breed, birthday, health info, and more to keep your pet’s details organized.",

  "emergency": "In the app, go to 'Emergency Contacts' to view a list of nearby 24/7 vets, ambulance services, and pet helplines.",

  "marketplace": "While currently focused on services and social features, a pet product marketplace is under development. Stay tuned!",

  "report_content": "To report any inappropriate content:\n- Tap the three-dot menu on the post or profile.\n- Select 'Report'.\n- Our moderation team will review and act promptly.",

  "training": "Visit the 'Tips & Training' section in PupHub for expert videos, blogs, and how-to guides on training your pet effectively.",

  "multi_pet": "Yes, you can create multiple pet profiles in PupHub. Manage details for each pet under your main account.",

  "languages": "Currently, PupHub supports English. Support for more Indian languages is coming soon!",
  "developer": "PupHub is developed and maintained by Apexium Technologies Pvt. Ltd., a company specializing in mobile and web app development. For collaboration or inquiries, contact us at hello@apexium.tech."

};

export default function App() {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<{ role: 'user' | 'model'; text: string }[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = { role: 'user', text: inputText };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputText('');
    setLoading(true);

    const lowerInput = inputText.toLowerCase();
    const manualKey = Object.keys(CUSTOM_RESPONSES).find(key =>
      lowerInput.includes(key)
    );

    if (manualKey) {
      setMessages([...newMessages, { role: 'model', text: CUSTOM_RESPONSES[manualKey] }]);
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [
            {
              parts: [{ text: inputText }],
            },
          ],
        }),
      });

      const data = await response.json();
      const reply =
        data?.candidates?.[0]?.content?.parts?.[0]?.text || 'No response from Gemini.';

      setMessages([...newMessages, { role: 'model', text: reply }]);
    } catch (error) {
      console.error('API Error:', error);
      setMessages([...newMessages, { role: 'model', text: 'Error connecting to Gemini API.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={messages}
        keyExtractor={(_, index) => index.toString()}
        contentContainerStyle={styles.chatContainer}
        renderItem={({ item }) => (
          <View
            style={[
              styles.messageBubble,
              item.role === 'user' ? styles.userBubble : styles.modelBubble,
            ]}
          >
            <Text style={styles.messageText}>{item.text}</Text>
          </View>
        )}
      />
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        keyboardVerticalOffset={80}
        style={styles.inputContainer}
      >
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Ask about PupHub or pets..."
        />
        <Button title={loading ? '...' : 'Send'} onPress={sendMessage} disabled={loading} />
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  chatContainer: { padding: 10 },
  messageBubble: {
    padding: 10,
    borderRadius: 8,
    marginBottom: 10,
    maxWidth: '80%',
  },
  userBubble: {
    backgroundColor: '#dcf8c6',
    alignSelf: 'flex-end',
  },
  modelBubble: {
    backgroundColor: '#e5e5ea',
    alignSelf: 'flex-start',
  },
  messageText: { fontSize: 16 },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    borderTopWidth: 1,
    borderColor: '#ccc',
    backgroundColor: '#f9f9f9',
    alignItems: 'center',
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 20,
    paddingHorizontal: 15,
    marginRight: 10,
    backgroundColor: '#fff',
  },
});
