import { SafeAreaView, StyleSheet } from 'react-native';
import AppNavigator from './src/navigation/AppNavigator';
import colors from './src/theme/colors';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <AppNavigator />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bg,
  },
});
