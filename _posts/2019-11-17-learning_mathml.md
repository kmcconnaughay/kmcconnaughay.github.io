---
layout: post
title: Learning MathML
---

Going forward, I expect that math will be a subject I discuss on this blog. Before discussing it,
though, I needed to learn how to display math formulas in the browser. Based on my research, there
are a few approaches one can take:

1. Render your formluas in TeX (or similar) and display them as images.</li>
1. Use a JavaScript library like [MathJax](https://www.mathjax.org/) to render TeX equations (or
   similar) as SVG images, HTML+CSS, and/or [MathML](https://en.wikipedia.org/wiki/MathML), an
   ISO-standard XML schema for math equations, in the client's browser.
1. Do something dumb like hand-write your equations in MathML, breaking your website's cross-browser
   compatibility in the process because, despite the fact that the HTML5 standard has included
   MathML since 2015, Chrome and its variants (Edge, Safari, Brave, etc.) still do not support it.

Naturally I settled on the third option because, before today, I had never heard of MathML and I was
curious. To learn the basics, I decided to transcribe the
[Cauchy-Schwarz inequality](https://w.wiki/D8sK) because it appears in the first few pages of my
copy of
_[Principles of Mathematical Analysis](https://www.goodreads.com/book/show/292079.Principles_of_Mathematical_Analysis)_
and I lacked the motivation to look any further.

Note that as of November 17th, 2019 Firefox is the only browser that
[fully supports MathML](https://developer.mozilla.org/en-US/docs/Web/MathML/Element/math#Browser_compatibility).
If your browser does not correctly render what follows,
[here](/assets/images/cauchy-schwarz-inequality.png) is a screenshot of the equations as rendered by
Firefox.

<p>
Given
  <math>
    <mrow>
      <mrow>
        <msub>
          <mi>a</mi>
          <mn>1</mn>
        </msub>
        <mo> &hellip;</mo>
        <msub>
          <mi>a</mi>
          <mi>n</mi>
        </msub>
      </mrow>
      <mo>&isin;</mo>
      <mi>&#x2102;<!--DOUBLE-STRUCK CAPITAL C--></mi>
    </mrow>
  </math>
  and
  <math>
    <mrow>
      <mrow>
        <msub>
          <mi>b</mi>
          <mn>1</mn>
        </msub>
        <mo>&hellip;</mo>
        <msub>
          <mi>b</mi>
          <mi>n</mi>
        </msub>
      </mrow>
      <mo>&isin;</mo>
      <mi>&#x2102;<!--DOUBLE-STRUCK CAPITAL C--></mi>
    </mrow>
  </math>
  , where
  <math>
    <mover>
      <mi>z</mi>
      <mo>&oline;</mo>
    </mover>
  </math>
  is the complex conjugate of
  <math>
    <mrow>
      <mi>z</mi>
      <mo>&isin;</mo>
      <mi>&#x2102;<!--DOUBLE-STRUCK CAPITAL C--></mi>
    </mrow>
  </math>
  and
  <math>
    <mrow>
      <mrow>
        <mo>|</mo>
        <mi>z</mi>
        <mo>|</mo>
      </mrow>
      <mo>=</mo>
      <msup>
        <mrow>
          <mo>(</mo>
          <mi>z</mi>
          <mo>&#x2062;<!--INVISIBLE TIMES--></mo>
          <mover>
            <mi>z</mi>
            <mo>&oline;</mo>
          </mover>
          <mo>)</mo>
        </mrow>
        <mfrac>
          <mn>1</mn>
          <mn>2</mn>
        </mfrac>
      </msup>
    </mrow>
  </math>
  is the absolute value of <math><mi>z</mi></math>, the Cauchy-Schwarz Inequality is the
  following:
</p>

<math  display="block" id="cauchy-schwarz-inequality">
  <mrow>
    <msup>
      <mrow>
        <mrow>
          <mo>|</mo>
          <munderover>
            <mo>&sum;</mo>
            <mrow>
              <mi>j</mi>
              <mo>=</mo>
              <mn>1</mn>
            </mrow>
            <mi>n</mi>
          </munderover>
          <mrow>
            <msub>
              <mi>a</mi>
              <mi>j</mi>
            </msub>
            <mo>&#x2062;<!--INVISIBLE TIMES--></mo>
            <msub>
              <mover>
                <mi>b</mi>
                <mo>&oline;</mo>
              </mover>
              <mi>j</mi>
            </msub>
          </mrow>
          <mo>|</mo>
        </mrow>
      </mrow>
      <mn>2</mn>
    </msup>
    <mo>&le;</mo>
    <mrow>
      <mrow>
        <munderover>
          <mo>&sum;</mo>
          <mrow>
            <mi>j</mi>
            <mo>=</mo>
            <mn>1</mn>
          </mrow>
          <mi>n</mi>
        </munderover>
        <msup>
          <mrow>
            <mo>|</mo>
            <msub>
              <mi>a</mi>
              <mi>j</mi>
            </msub>
            <mo>|</mo>
          </mrow>
          <mn>2</mn>
        </msup>
      </mrow>
      <mo>&#x2062;<!--INVISIBLE TIMES--></mo>
      <mrow>
        <munderover>
          <mo>&sum;</mo>
          <mrow>
            <mi>j</mi>
            <mo>=</mo>
            <mn>1</mn>
          </mrow>
          <mi>n</mi>
        </munderover>
        <msup>
          <mrow>
            <mo>|</mo>
            <msub>
              <mi>b</mi>
              <mi>j</mi>
            </msub>
            <mo>|</mo>
          </mrow>
          <mn>2</mn>
        </msup>
      </mrow>
    </mrow>
  </mrow>
</math>

If you'd like to see the many lines of MathML that produced this equation, search for the string
"cauchy-schwarz-inequality" in the page source, which you can view in the browser or on
[GitHub](https://github.com/kmcconnaughay/kmcconnaughay.github.io/blob/main/_posts/2019-11-17-learning-mathml.md).

Here are some takeaways from this exercise:

- [HTML named entities](https://w.wiki/MPES) allow you to insert otherwise difficult-to-type symbols
  into your markup. For example, "∑", the capital Greek letter sigma oft used in summations, is
  written <code class="inline-code">&amp;sum;</code> in HTML.
- For Unicode symbols that lack a named HTML entity, you can use their Unicode encoding directly.
  For example, "ℂ", the symbol commonly used to represent the set of complex numbers, is written
  `&sum;` in HTML.
- MathML is verbose, but powerful. It comes with its own set of dedicated XML tags, like `<mfrac>`
  for fractions and `msup` for superscript, that allow you to construct arbitrarily complex
  equations. I appreciate that Firefox does this in vanilla HTML without the need for heavy
  JavaScript polyfills.
- Because MathML is verbose, writing it by hand is error-prone. I did my best write it semantically,
  but it's <s>possible</s> probable that I missed an `<mrow>` tag or made other, less obvious
  errors. In the future I might use a TeX to MathML converter to generate the markup, instead.
- I need to find a good HTML formatter and a static page templater to make writing new posts easier.
  I'm not going to use a managed solution like WordPress because half the point of this website is
  to learn new things from first principles, but I think some minimal tooling will make my life
  easier.
