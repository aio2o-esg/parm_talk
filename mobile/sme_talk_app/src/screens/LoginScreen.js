import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity,
  StyleSheet, ActivityIndicator
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import colors from '../theme/colors';

export default function LoginScreen({ onLoginSuccess }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    // 테스트용 바로 로그인 (백엔드 연동 전)
    await AsyncStorage.setItem('access_token', 'test_token');
    onLoginSuccess();
  };

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>🌿 SME-TALK</Text>
      <Text style={styles.subtitle}>ESG-Gold Platform · Algorand</Text>

      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="이메일 또는 사업자번호"
          placeholderTextColor={colors.textMuted}
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder="비밀번호"
          placeholderTextColor={colors.textMuted}
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <TouchableOpacity
          style={styles.loginBtn}
          onPress={handleLogin}
          disabled={loading}
        >
          {loading
            ? <ActivityIndicator color={colors.black} />
            : <Text style={styles.loginBtnText}>로그인</Text>
          }
        </TouchableOpacity>

        <TouchableOpacity style={styles.walletBtn}>
          <Text style={styles.walletBtnText}>🔗 Algorand 지갑 연결</Text>
        </TouchableOpacity>

        <Text style={styles.register}>계정이 없으신가요? 회원가입</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bg,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  logo: {
    fontSize: 32,
    fontWeight: 'bold',
    color: colors.gold,
  },
  subtitle: {
    fontSize: 13,
    color: colors.textMuted,
    marginBottom: 32,
  },
  form: {
    width: '100%',
    gap: 12,
  },
  input: {
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 12,
    padding: 14,
    color: colors.text,
    fontSize: 14,
  },
  loginBtn: {
    backgroundColor: colors.gold,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  loginBtnText: {
    color: colors.black,
    fontWeight: 'bold',
    fontSize: 16,
  },
  walletBtn: {
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.gold,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  walletBtnText: {
    color: colors.gold,
    fontWeight: 'bold',
    fontSize: 14,
  },
  register: {
    color: colors.textMuted,
    textAlign: 'center',
    fontSize: 13,
    marginTop: 8,
  },
});