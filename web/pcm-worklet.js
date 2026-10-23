class Capture extends AudioWorkletProcessor{
 constructor(){super();this.samples=[];this.pos=0;this.chunk=[]}
 process(inputs){const input=inputs[0]?.[0];if(!input)return true;this.samples.push(...input);const step=sampleRate/16000;while(this.pos+1<this.samples.length){const a=Math.floor(this.pos),f=this.pos-a;this.chunk.push(this.samples[a]*(1-f)+this.samples[a+1]*f);this.pos+=step;if(this.chunk.length===640){const out=new Float32Array(this.chunk);this.port.postMessage(out,[out.buffer]);this.chunk=[]}}const used=Math.floor(this.pos);this.samples.splice(0,used);this.pos-=used;return true}
}
registerProcessor('pcm-capture',Capture);
