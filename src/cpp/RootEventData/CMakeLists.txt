add_library(RootEventData SHARED
	src/TBossFullEvent.cxx
	src/TDigiEvent.cxx
	src/TDisTrack.cxx
	src/TDstEvent.cxx
	src/TDstHltInf.cxx
	src/TEmcDigi.cxx
	src/TEmcMc.cxx
	src/TEmcTrack.cxx
	src/TEvtHeader.cxx
	src/TEvtNavigator.cxx
	src/TEvtRecDTag.cxx
	src/TEvtRecEtaToGG.cxx
	src/TEvtRecEvent.cxx
	src/TEvtRecObject.cxx
	src/TEvtRecPi0.cxx
	src/TEvtRecPrimaryVertex.cxx
	src/TEvtRecTrack.cxx
	src/TEvtRecVeeVertex.cxx
	src/TExtTrack.cxx
	src/THltEvent.cxx
	src/THltInf.cxx
	src/THltRaw.cxx
	src/TJobInfo.cxx
	src/TLumiDigi.cxx
	src/TMcDigiEmc.cxx
	src/TMcEvent.cxx
	src/TMcHitEvent.cxx
	src/TMcHitMdc.cxx
	src/TMcHitTof.cxx
	src/TMcParticle.cxx
	src/TMdcDedx.cxx
	src/TMdcDigi.cxx
	src/TMdcKalTrack.cxx
	src/TMdcMc.cxx
	src/TMdcTrack.cxx
	src/TMucDigi.cxx
	src/TMucMc.cxx
	src/TMucTrack.cxx
	src/TRawData.cxx
	src/TRecEmcCluster.cxx
	src/TRecEmcHit.cxx
	src/TRecEmcShower.cxx
	src/TRecEvTime.cxx
	src/TRecExtTrack.cxx
	src/TRecMdcDedx.cxx
	src/TRecMdcDedxHit.cxx
	src/TRecMdcHit.cxx
	src/TRecMdcKalHelixSeg.cxx
	src/TRecMdcKalTrack.cxx
	src/TRecMdcTrack.cxx
	src/TRecMucTrack.cxx
	src/TRecTofTrack.cxx
	src/TRecTrackEvent.cxx
	src/TRecZddChannel.cxx
	src/TTofDigi.cxx
	src/TTofMc.cxx
	src/TTofTrack.cxx
	src/TTrigData.cxx
	src/TTrigEvent.cxx		
)

target_include_directories(RootEventData PUBLIC
	$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
	$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

target_link_libraries(RootEventData PUBLIC
	ROOT::Core
	ROOT::Physics
)

install(
	TARGETS RootEventData
	EXPORT ${PROJECT_NAME}Targets
	LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)


#[===============================[
	Generate ROOT dictionary
#]===============================]

file(GLOB RootEventData_dict_headers include/RootEventData/T*.h)
ROOT_GENERATE_DICTIONARY(RootEventDataDict
	${RootEventData_dict_headers}
	LINKDEF include/RootEventData/LinkDef.h
	MODULE RootEventData
)

install(
	FILES
		${CMAKE_CURRENT_BINARY_DIR}/libRootEventData_rdict.pcm
		${CMAKE_CURRENT_BINARY_DIR}/libRootEventData.rootmap
	DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
