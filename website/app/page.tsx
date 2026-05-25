import React from 'react'
import Hero from '@/features/homepage/Hero'
import Marquee from '@/features/homepage/Marquee'
import Features from '@/features/homepage/Features'
import HowItWorks from '@/features/homepage/HowItWorks'
import Testimonials from '@/features/homepage/Testimonials'
import CTA from '@/features/homepage/Cta'

const page = () => {
  return (
    <>
    <Hero/>
    <Marquee/>
    <Features/>
    <HowItWorks/>
    <Testimonials/>
    <CTA/>
    </>
  )
}

export default page