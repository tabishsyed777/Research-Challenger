"""Research, adversarial review, and revision over supplied evidence."""
import argparse, json
from engine import Agent, save

def validate_sources(sources):
    if not isinstance(sources,list) or not sources: raise ValueError('Evidence is required')
    ids=set()
    for s in sources:
        if not isinstance(s,dict) or not all(isinstance(s.get(k),str) and s[k].strip() for k in ('id','title','text')):
            raise ValueError('Each source needs id, title, text')
        if s['id'] in ids: raise ValueError('Duplicate source ID')
        ids.add(s['id'])
    return ids

def validate_claims(result, ids):
    claims=result.get('claims')
    if not isinstance(claims,list) or not claims: raise ValueError('Claims required')
    for c in claims:
        if not isinstance(c,dict) or not isinstance(c.get('text'),str) or not c['text'].strip(): raise ValueError('Claim text required')
        refs=c.get('citations')
        if not isinstance(refs,list) or not refs or any(not isinstance(r,str) or r not in ids for r in refs):
            raise ValueError('Every claim must cite supplied source IDs')
    return claims

def research(question,sources,agent):
    ids=validate_sources(sources)
    if not question.strip(): raise ValueError('Question required')
    demo=[{'text':s['text'],'citations':[s['id']]} for s in sources]
    draft=agent.run('Researcher: answer only from evidence; return claims [{text,citations:[source IDs]}].',
        dict(question=question,sources=sources),{'claims':demo})
    validate_claims(draft,ids)
    review=agent.run('Challenger: find contradictions and overclaims; return concerns as a list of strings.',
        dict(question=question,sources=sources,draft=draft),
        {'concerns':['Synthetic examples are not real-world findings.','Small pilots cannot establish general effectiveness.']})
    concerns=review.get('concerns')
    if not isinstance(concerns,list) or any(not isinstance(c,str) for c in concerns): raise ValueError('Invalid concerns')
    final=agent.run('Editor: revise using critique. Return claims [{text,citations:[source IDs]}] and limitations as a list of strings.',
        dict(question=question,sources=sources,draft=draft,critique=review),{'claims':demo,'limitations':concerns})
    validate_claims(final,ids)
    limits=final.get('limitations')
    if not isinstance(limits,list) or any(not isinstance(c,str) for c in limits): raise ValueError('Invalid limitations')
    return dict(question=question,mode='live' if agent.live else 'scripted demo',claims=final['claims'],limitations=limits,
        critique=concerns,sources=sources,citation_check='IDs verified; semantic support requires review.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live',action='store_true')
    parser.add_argument('--question',default='Does a four-day workweek improve productivity?')
    parser.add_argument('--sources',default='examples/sources.json')
    parser.add_argument('--out',default='work/research-challenger')
    args=parser.parse_args()
    agent=Agent(args.live)
    with open(args.sources) as f: sources=json.load(f)
    report=research(args.question,sources,agent)
    save(args.out,report,agent)
    print(json.dumps(report,indent=2))
