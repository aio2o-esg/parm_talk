import React, { useState } from 'react';
import {
  View, Text, ScrollView, TouchableOpacity,
  StyleSheet, Alert
} from 'react-native';
import colors from '../theme/colors';
import BottomNav from '../components/BottomNav';

const CYCLE_STEPS = [
  { label: '데이터 수집', icon: '📡', key: 'collect' },
  { label: 'AI 분석', icon: '🤖', key: 'analyze' },
  { label: '정책 판단', icon: '⚖️', key: 'decide' },
  { label: '온체인 실행', icon: '⛓️', key: 'execute' },
];

const PARAMS = [
  { key: 'reward_rate_env', label: '환경 활동 보상 배율', value: 0.07, max: 0.2 },
  { key: 'sme_bonus_rate', label: '소상공인 우대 보너스', value: 0.10, max: 0.3 },
  { key: 'anomaly_threshold', label: '이상행위 탐지 임계값', value: 0.15, max: 1.0 },
  { key: 'monthly_issue_cap', label: '월간 Gold 발행 한도', value: 10000, max: 50000 },
];

const AI_RESULTS = [
  { label: '참여율 변화', value: '▲ +12.4%', positive: true },
  { label: '이상행위 탐지', value: '3건', positive: false },
  { label: '다음 주 예측 발행량', value: '12,400 ESGG', positive: true },
  { label: '정책 효과 점수', value: '78.5점', positive: true },
];

export default function PolicyScreen({ user, onNavigate }) {
  const [activeStep, setActiveStep] = useState('analyze');
  const isAdmin = user?.userType === 'admin';

  const handleApprove = () => {
    Alert.alert(
      '정책 파라미터 변경 승인',
      'AI 분석 결과에 따른 파라미터 변경을 승인하시겠습니까?\n\nKubernetes ConfigMap이 업데이트되고 Rolling Update가 실행됩니다.',
      [
        { text: '취소', style: 'cancel' },
        { text: '승인', onPress: () => Alert.alert('승인 완료', '새로운 정책이 무중단으로 적용되었습니다.') },
      ]
    );
  };

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scroll} showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <Text style={styles.title}>AI 정책 대시보드</Text>
          <View style={styles.badge}>
            <Text style={styles.badgeText}>🤖 AI Policy Engine</Text>
          </View>
        </View>

        {/* 정책 환류 사이클 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>정책 환류 사이클</Text>
          <View style={styles.cycle}>
            {CYCLE_STEPS.map((step, i) => (
              <React.Fragment key={step.key}>
                <TouchableOpacity
                  style={[styles.cycleStep, activeStep === step.key && styles.cycleStepActive]}
                  onPress={() => setActiveStep(step.key)}
                >
                  <Text style={styles.cycleIcon}>{step.icon}</Text>
                  <Text style={[
                    styles.cycleLabel,
                    activeStep === step.key && styles.cycleLabelActive
                  ]}>
                    {step.label}
                  </Text>
                </TouchableOpacity>
                {i < CYCLE_STEPS.length - 1 && (
                  <Text style={styles.cycleArrow}>→</Text>
                )}
              </React.Fragment>
            ))}
          </View>
        </View>

        {/* 정책 파라미터 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>현재 정책 파라미터</Text>
          {PARAMS.map(param => (
            <View key={param.key} style={styles.paramItem}>
              <View style={styles.paramHeader}>
                <Text style={styles.paramLabel}>{param.label}</Text>
                <Text style={styles.paramValue}>{param.value}</Text>
              </View>
              <View style={styles.paramTrack}>
                <View style={[
                  styles.paramFill,
                  { width: `${(param.value / param.max) * 100}%` }
                ]} />
              </View>
            </View>
          ))}
        </View>

        {/* AI 분석 결과 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>AI 분석 결과 요약</Text>
          <View style={styles.resultsGrid}>
            {AI_RESULTS.map((result, i) => (
              <View key={i} style={styles.resultItem}>
                <Text style={styles.resultLabel}>{result.label}</Text>
                <Text style={[
                  styles.resultValue,
                  result.positive ? styles.resultPositive : styles.resultNegative
                ]}>
                  {result.value}
                </Text>
              </View>
            ))}
          </View>
        </View>

        {/* 관리자 전용 승인 버튼 */}
        {isAdmin && (
          <TouchableOpacity style={styles.approveBtn} onPress={handleApprove}>
            <Text style={styles.approveBtnText}>⚙️ 정책 파라미터 변경 승인</Text>
            <Text style={styles.approveBtnSub}>ConfigMap 업데이트 → Rolling Update</Text>
          </TouchableOpacity>
        )}

        {!isAdmin && (
          <View style={styles.infoBox}>
            <Text style={styles.infoText}>
              💡 정책 파라미터 변경 승인은 지자체 관리자만 가능합니다.
            </Text>
          </View>
        )}
      </ScrollView>

      <BottomNav active="policy" onPress={onNavigate} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bg },
  scroll: { flex: 1, padding: 20 },
  header: { marginBottom: 16 },
  title: { color: colors.gold, fontSize: 22, fontWeight: 'bold' },
  badge: {
    backgroundColor: colors.surfaceLight, borderRadius: 20,
    paddingHorizontal: 12, paddingVertical: 4,
    alignSelf: 'flex-start', marginTop: 6,
    borderWidth: 1, borderColor: colors.gold,
  },
  badgeText: { color: colors.gold, fontSize: 12 },
  section: {
    backgroundColor: colors.surface, borderRadius: 16,
    padding: 16, marginBottom: 16,
    borderWidth: 1, borderColor: colors.border,
  },
  sectionTitle: { color: colors.gold, fontSize: 14, fontWeight: 'bold', marginBottom: 14 },
  cycle: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  cycleStep: {
    alignItems: 'center', padding: 8,
    borderRadius: 12, flex: 1,
  },
  cycleStepActive: { backgroundColor: colors.surfaceLight, borderWidth: 1, borderColor: colors.gold },
  cycleIcon: { fontSize: 20, marginBottom: 4 },
  cycleLabel: { color: colors.textMuted, fontSize: 9, textAlign: 'center' },
  cycleLabelActive: { color: colors.gold },
  cycleArrow: { color: colors.textDim, fontSize: 14, paddingHorizontal: 2 },
  paramItem: { marginBottom: 14 },
  paramHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 6 },
  paramLabel: { color: colors.text, fontSize: 12 },
  paramValue: { color: colors.goldLight, fontSize: 12, fontWeight: 'bold' },
  paramTrack: {
    height: 8, backgroundColor: colors.surfaceLight,
    borderRadius: 4, overflow: 'hidden',
  },
  paramFill: { height: '100%', backgroundColor: colors.gold, borderRadius: 4 },
  resultsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  resultItem: {
    backgroundColor: colors.surfaceLight, borderRadius: 12,
    padding: 12, width: '47%',
  },
  resultLabel: { color: colors.textMuted, fontSize: 11, marginBottom: 6 },
  resultValue: { fontSize: 16, fontWeight: 'bold' },
  resultPositive: { color: colors.success },
  resultNegative: { color: colors.danger },
  approveBtn: {
    backgroundColor: colors.gold, borderRadius: 16,
    padding: 18, alignItems: 'center', marginBottom: 16,
  },
  approveBtnText: { color: colors.black, fontSize: 16, fontWeight: 'bold' },
  approveBtnSub: { color: colors.black, fontSize: 11, marginTop: 4, opacity: 0.7 },
  infoBox: {
    backgroundColor: colors.surface, borderRadius: 12,
    padding: 14, marginBottom: 16,
    borderWidth: 1, borderColor: colors.border,
  },
  infoText: { color: colors.textMuted, fontSize: 13, textAlign: 'center' },
});