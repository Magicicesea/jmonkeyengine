#import "Common/ShaderLib/PssmShadows.glsllib"

uniform sampler2D m_Texture;
uniform sampler2D m_DepthTexture;
uniform mat4 m_ViewProjectionMatrixInverse;
uniform vec4 m_ViewProjectionMatrixRow2;

varying vec2 texCoord;


const mat4 biasMat = mat4(0.5, 0.0, 0.0, 0.0,
                          0.0, 0.5, 0.0, 0.0,
                          0.0, 0.0, 0.5, 0.0,
                          0.5, 0.5, 0.5, 1.0);

uniform mat4 m_LightViewProjectionMatrix0;
uniform mat4 m_LightViewProjectionMatrix1;
uniform mat4 m_LightViewProjectionMatrix2;
uniform mat4 m_LightViewProjectionMatrix3;

#ifdef POINTLIGHT
    uniform vec3 m_LightPos;
    uniform mat4 m_LightViewProjectionMatrix4;
    uniform mat4 m_LightViewProjectionMatrix5;
#endif

#ifdef FADE
uniform vec2 m_FadeInfo;
#endif

vec3 getPosition(in float depth, in vec2 uv){
    vec4 pos = vec4(uv, depth, 1.0) * 2.0 - 1.0;
    pos = m_ViewProjectionMatrixInverse * pos;
    return pos.xyz / pos.w;
}

void main(){    
    
    float depth = texture2D(m_DepthTexture,texCoord).r;
    vec4 color = texture2D(m_Texture,texCoord);

    //Discard shadow computation on the sky
    if(depth == 1.0){
        gl_FragColor = color;
        return;
    }

    // get the vertex in world space
    vec4 worldPos = vec4(getPosition(depth,texCoord),1.0);
  
    // populate the light view matrices array and convert vertex to light viewProj space
    vec4 projCoord0 = biasMat * m_LightViewProjectionMatrix0 * worldPos;
    vec4 projCoord1 = biasMat * m_LightViewProjectionMatrix1 * worldPos;
    vec4 projCoord2 = biasMat * m_LightViewProjectionMatrix2 * worldPos;
    vec4 projCoord3 = biasMat * m_LightViewProjectionMatrix3 * worldPos;
    #ifdef POINTLIGHT
       vec4 projCoord4 = biasMat * m_LightViewProjectionMatrix4 * worldPos;
       vec4 projCoord5 = biasMat * m_LightViewProjectionMatrix5 * worldPos;
    #endif

    float shadow = 1.0;
    #ifdef PSSM
        float shadowPosition = m_ViewProjectionMatrixRow2.x * worldPos.x +  m_ViewProjectionMatrixRow2.y * worldPos.y +  m_ViewProjectionMatrixRow2.z * worldPos.z +  m_ViewProjectionMatrixRow2.w;

        if(shadowPosition < m_Splits.x){
            shadow = GETSHADOW(m_ShadowMap0, projCoord0);
        }else if( shadowPosition <  m_Splits.y){
            shadowBorderScale = 0.5;
            shadow = GETSHADOW(m_ShadowMap1, projCoord1);
        }else if( shadowPosition <  m_Splits.z){
            shadowBorderScale = 0.25;
            shadow = GETSHADOW(m_ShadowMap2, projCoord2);
        }else if( shadowPosition <  m_Splits.w){
            shadowBorderScale = 0.125;
            shadow = GETSHADOW(m_ShadowMap3, projCoord3);
        }
    #endif

    #ifdef POINTLIGHT         
         vec3 vect = worldPos.xyz - m_LightPos;
         vec3 absv= abs(vect);
         float maxComp = max(absv.x,max(absv.y,absv.z));
         if(maxComp == absv.y){
            if(vect.y < 0.0){
                shadow = GETSHADOW(m_ShadowMap0, projCoord0);             
            }else{
                shadow = GETSHADOW(m_ShadowMap1, projCoord1);
            }
         }else if(maxComp == absv.z){
            if(vect.z < 0.0){
                shadow = GETSHADOW(m_ShadowMap2, projCoord2);
            }else{
                shadow = GETSHADOW(m_ShadowMap3, projCoord3);
            }
         }else if(maxComp == absv.x){
            if(vect.x < 0.0){
                shadow = GETSHADOW(m_ShadowMap4, projCoord4);
            }else{
                shadow = GETSHADOW(m_ShadowMap5, projCoord5);
            }
         }                  
    #endif   

    #ifdef FADE
      shadow = max(0.0,mix(shadow,1.0,(shadowPosition - m_FadeInfo.x) * m_FadeInfo.y));    
    #endif    
    shadow= shadow * m_ShadowIntensity + (1.0 - m_ShadowIntensity);
    gl_FragColor = color * vec4(shadow, shadow, shadow, 1.0);

}

