import React, { useState, useEffect } from 'react';
import { View, ActivityIndicator } from 'react-native';
import colors from '../theme/colors';
import SplashScreen from '../screens/SplashScreen';
import LoginScreen from '../screens/LoginScreen';
import HomeScreen from '../screens/HomeScreen';
import ESGVerifyScreen from '../screens/ESGVerifyScreen';
import WalletScreen from '../screens/WalletScreen';
import PolicyScreen from '../screens/PolicyScreen';
import MyPageScreen from '../screens/MyPageScreen';

const DUMMY_USER = {
  name: '성보경',
  userType: 'admin',
  region: '서울시',
};

export default function AppNavigator() {
  const [appState, setAppState] = useState('splash');
  const [currentScreen, setCurrentScreen] = useState('home');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          setUser(DUMMY_USER);
          setAppState('app');
        }
      } catch (e) {
        console.log(e);
      } finally {
        setLoading(false);
      }
    }, 100);
    return () => clearTimeout(timer);
  }, []);

  const screenProps = {
    user,
    onNavigate: setCurrentScreen,
    onLogout: () => {
      setUser(null);
      setAppState('login');
    },
  };

  if (loading) {
    return (
      <View style={{ flex: 1, backgroundColor: colors.bg,
        alignItems: 'center', justifyContent: 'center' }}>
        <ActivityIndicator color={colors.gold} size="large" />
      </View>
    );
  }

  if (appState === 'splash') {
    return <SplashScreen onFinish={() => setAppState('login')} />;
  }

  if (appState === 'login') {
    return (
      <LoginScreen
        onLoginSuccess={() => {
          setUser(DUMMY_USER);
          setAppState('app');
        }}
      />
    );
  }

  if (currentScreen === 'activity') return <ESGVerifyScreen {...screenProps} />;
  if (currentScreen === 'wallet') return <WalletScreen {...screenProps} />;
  if (currentScreen === 'policy') return <PolicyScreen {...screenProps} />;
  if (currentScreen === 'mypage') return <MyPageScreen {...screenProps} />;

  return <HomeScreen {...screenProps} />;
}
